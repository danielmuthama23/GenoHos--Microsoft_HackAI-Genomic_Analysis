import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from openai import AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OPENAI_GPT4_DEPLOYMENT = os.getenv("OPENAI_GPT4_DEPLOYMENT")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ADA_DEPLOYMENT = os.getenv("OPENAI_ADA_DEPLOYMENT")

KUSTO_URI = os.getenv("KUSTO_URI")
KUSTO_DATABASE = os.getenv("KUSTO_DATABASE")
KUSTO_TABLE = os.getenv("KUSTO_TABLE")

# Azure Authentication
credential = DefaultAzureCredential()

# # Kusto Client
# kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
#     KUSTO_URI,
#     application_client_id=os.getenv("AZURE_CLIENT_ID"),
#     application_key=os.getenv("AZURE_CLIENT_SECRET"),
#     authority_id=os.getenv("AZURE_TENANT_ID")
# )

# Use this universal approach that works with most versions
kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
    KUSTO_URI,
    os.getenv("AZURE_CLIENT_ID"),
    os.getenv("AZURE_CLIENT_SECRET"),
    os.getenv("AZURE_TENANT_ID")
)

kusto_client = KustoClient(kcsb)

# OpenAI Client
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY,
    api_version="2023-09-01-preview"
)

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def generate_embeddings(text: str) -> list:
    try:
        response = openai_client.embeddings.create(
            input=[text.replace("\n", " ")],
            model=OPENAI_ADA_DEPLOYMENT
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding generation failed: {str(e)}")
        return None

def execute_kusto_query(query: str) -> list:
    try:
        response = kusto_client.execute(KUSTO_DATABASE, query)
        return [row.to_dict() for row in response.primary_results[0]]
    except Exception as e:
        print(f"Kusto query failed: {str(e)}")
        return []

def query_biospecimen_data(question: str, top_results: int = 3) -> dict:
    embedding = generate_embeddings(question)
    if not embedding:
        return {"answer": "Embedding generation failed", "sources": []}

    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    kusto_query = f"""
    {KUSTO_TABLE}
    | extend similarity = cosine_similarity(embedding, dynamic({embedding_str}))
    | top {top_results} by similarity desc
    | project content, metadata, similarity
    """
    
    results = execute_kusto_query(kusto_query)
    if not results:
        return {"answer": "No relevant records found", "sources": []}

    context = "\n".join([
        f"Record {idx+1} (Similarity: {row['similarity']:.2f}):\n"
        f"Content: {row['content']}\n"
        f"Metadata: {json.dumps(row['metadata'])}\n"
        for idx, row in enumerate(results)
    ])

    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_GPT4_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a biomedical research assistant. "
                 "Use only the provided context to answer questions about breast cancer biospecimens."},
                {"role": "user", "content": f"Question: {question}\nContext:\n{context}"}
            ],
            temperature=0.2,
            max_tokens=500
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"LLM processing error: {str(e)}"

    return {
        "answer": answer,
        "sources": [{
            "content": r["content"],
            "metadata": r["metadata"],
            "similarity": round(r["similarity"], 2)
        } for r in results],
        "processing_time": f"{len(results)} results analyzed"
    }

class QueryRequest(BaseModel):
    question: str
    top_results: int = 3

@app.post("/query")
async def handle_query(request: QueryRequest):
    try:
        result = query_biospecimen_data(request.question, request.top_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "biospecimen-query"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))