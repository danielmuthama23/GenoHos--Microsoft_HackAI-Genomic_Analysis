import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from openai import AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

app = FastAPI()

# ========== Configuration ==========
# Get credentials from environment variables
OPENAI_GPT4_DEPLOYMENT = os.getenv("OPENAI_GPT4_DEPLOYMENT")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ADA_DEPLOYMENT = os.getenv("OPENAI_ADA_DEPLOYMENT")

KUSTO_URI = os.getenv("KUSTO_URI")
KUSTO_DATABASE = os.getenv("KUSTO_DATABASE")
KUSTO_TABLE = os.getenv("KUSTO_TABLE")

# ========== Service Clients ==========
# Azure Authentication
credential = DefaultAzureCredential()

# Kusto Client (Corrected Parameters)
kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
    KUSTO_URI,
    application_client_id=os.getenv("AZURE_CLIENT_ID"),
    application_key=os.getenv("AZURE_CLIENT_SECRET"),
    authority_id=os.getenv("AZURE_TENANT_ID")
)
kusto_client = KustoClient(kcsb)

# OpenAI Client
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY,
    api_version="2023-09-01-preview"
)

# ========== Core Logic ==========
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def generate_embeddings(text: str) -> list:
    """Generate embeddings using OpenAI Ada model"""
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
    """Execute Kusto query and return results"""
    try:
        response = kusto_client.execute(KUSTO_DATABASE, query)
        return [row.to_dict() for row in response.primary_results[0]]
    except Exception as e:
        print(f"Kusto query failed: {str(e)}")
        return []

def query_biospecimen_data(question: str, top_results: int = 3) -> dict:
    """Main query processing pipeline"""
    # Generate question embedding
    embedding = generate_embeddings(question)
    if not embedding:
        return {"answer": "Embedding generation failed", "sources": []}

    # Build Kusto query
    kusto_query = f"""
    {KUSTO_TABLE}
    | extend similarity = cosine_similarity(embedding, {embedding})
    | top {top_results} by similarity desc
    | project content, metadata, similarity
    """
    
    # Execute query
    results = execute_kusto_query(kusto_query)
    if not results:
        return {"answer": "No relevant records found", "sources": []}

    # Prepare LLM context
    context = "\n".join([
        f"Record {idx+1} (Similarity: {row['similarity']:.2f}):\n"
        f"Content: {row['content']}\n"
        f"Metadata: {json.dumps(row['metadata'])}\n"
        for idx, row in enumerate(results)
    ])

    # Generate LLM response
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
        } for r in results]
    }

# ========== API Endpoints ==========
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

# ========== Entry Point ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))