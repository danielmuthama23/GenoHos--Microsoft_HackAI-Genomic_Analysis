from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from notebookutils import mssparkutils
from pyspark.sql import SparkSession
from openai import AzureOpenAI
import time
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
limiter = Limiter(app=app, key_func=get_remote_address)

# Initialize monitoring
configure_azure_monitor(
    connection_string=mssparkutils.credentials.getSecret("monitoring-scope", "APP_INSIGHTS_KEY"),
    logging_level=logging.INFO
)

# Initialize Spark
spark = SparkSession.builder.appName("BiospecimenAPI").getOrCreate()

class BiospecimenRAGSystem:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=mssparkutils.credentials.getSecret("openai-scope", "OPENAI_ENDPOINT"),
            api_key=mssparkutils.credentials.getSecret("openai-scope", "OPENAI_KEY"),
            api_version="2023-09-01-preview"
        )
        self.kusto_uri = "https://trd-zdxwqrcu1znbqygpxg.z2.kusto.fabric.microsoft.com"
        self.kusto_db = "BioEventHouse"
        
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def generate_embeddings(self, text):
        return self.client.embeddings.create(
            input=[text.replace("\n", " ")],
            model="text-embedding-ada-002"
        ).data[0].embedding
    
    def query_kusto(self, embedding, limit=3):
        query = f"""
        biospecimen_embeddings
        | extend similarity = series_cosine_similarity(dynamic({str(embedding)}), embedding)
        | top {limit} by similarity desc
        | project content, metadata, similarity
        """
        return spark.read \
            .format("com.microsoft.kusto.spark.synapse.datasource") \
            .option("kustoCluster", self.kusto_uri) \
            .option("kustoDatabase", self.kusto_db) \
            .option("accessToken", mssparkutils.credentials.getToken(self.kusto_uri)) \
            .option("kustoQuery", query) \
            .load()
    
    def generate_response(self, question, context):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a biomedical research assistant."},
                {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"}
            ],
            temperature=0.2,
            max_tokens=200
        )
        return response.choices[0].message.content

system = BiospecimenRAGSystem()

@app.route('/api/query', methods=['POST'])
@limiter.limit("10 per minute")
def handle_query():
    try:
        data = request.json
        question = data.get('question', '')
        
        start_time = time.time()
        embedding = system.generate_embeddings(question)
        results = system.query_kusto(embedding).collect()
        
        context = "\n".join([
            f"Document {idx+1} (Similarity: {row['similarity']:.2f}): {row['content']}"
            for idx, row in enumerate(results)
        ])
        
        answer = system.generate_response(question, context)
        
        return jsonify({
            "answer": answer,
            "sources": [dict(row.asDict()) for row in results],
            "processing_time": f"{time.time() - start_time:.2f}s"
        })
        
    except Exception as e:
        app.logger.error(f"Query failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    try:
        test_query = system.query_kusto(system.generate_embeddings("test"), 1)
        return jsonify({"status": "ready", "records": test_query.count()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)