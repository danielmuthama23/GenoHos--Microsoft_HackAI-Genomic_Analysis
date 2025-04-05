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
from tenacity import retry, wait_random_exponential, stop_after_attempt
from config import Config

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=[Config.RATE_LIMIT])

# Initialize monitoring
configure_azure_monitor(
    connection_string=Config.APP_INSIGHTS_KEY,
    logging_level=logging.INFO
)

# Initialize Spark with optimized configuration
spark = SparkSession.builder \
    .appName("BiospecimenAPI") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

class BiospecimenRAGSystem:
    def __init__(self):
        self.initialized = False
        self.embeddings_cache = {}
        self.kusto_token = mssparkutils.credentials.getToken(Config.KUSTO_URI)
        self.client = self._init_openai_client()
        self.initialize_system()
        
    def _init_openai_client(self):
        @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
        def _create_client():
            return AzureOpenAI(
                azure_endpoint=Config.OPENAI_ENDPOINT,
                api_key=Config.OPENAI_KEY,
                api_version=Config.OPENAI_API_VERSION
            )
        return _create_client()
    
    def initialize_system(self):
        """Check system readiness"""
        try:
            # Verify Kusto connection
            test_df = spark.read \
                .format("com.microsoft.kusto.spark.synapse.datasource") \
                .option("kustoCluster", Config.KUSTO_URI) \
                .option("kustoDatabase", Config.KUSTO_DB) \
                .option("accessToken", self.kusto_token) \
                .option("kustoQuery", f"{Config.KUSTO_TABLE} | count") \
                .load()
                
            if test_df.collect()[0][0] > 0:
                self.initialized = True
                app.logger.info("System initialized successfully")
            else:
                app.logger.error("No embeddings found in Eventhouse")
                
        except Exception as e:
            app.logger.error(f"Initialization failed: {str(e)}")
            raise

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def generate_embeddings(self, text):
        return self.client.embeddings.create(
            input=[text.replace("\n", " ")],
            model=Config.OPENAI_EMBEDDING_DEPLOYMENT
        ).data[0].embedding
    
    def query_kusto(self, embedding, limit=3):
        query = f"""
        {Config.KUSTO_TABLE}
        | extend similarity = series_cosine_similarity(dynamic({str(embedding)}), embedding)
        | top {limit} by similarity desc
        | project content=document_text, 
                 metadata=pack(
                    'sample_type', Sample_Type,
                    'primary_site', Primary_Site,
                    'aliquot_id', Aliquot_ID
                 ),
                 similarity
        """
        return spark.read \
            .format("com.microsoft.kusto.spark.synapse.datasource") \
            .option("kustoCluster", Config.KUSTO_URI) \
            .option("kustoDatabase", Config.KUSTO_DB) \
            .option("accessToken", self.kusto_token) \
            .option("kustoQuery", query) \
            .load()
    
    def generate_response(self, question, context):
        prompt = f"""You are a biomedical research assistant analyzing biospecimen data.
        
        Question: {question}
        
        Relevant Records:
        {context}
        
        Provide:
        1. A 1-2 sentence answer
        2. Key characteristics of matching samples
        3. Confidence assessment based on similarity scores"""
        
        response = self.client.chat.completions.create(
            model=Config.OPENAI_GPT4_DEPLOYMENT,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.2,
            max_tokens=250
        )
        return response.choices[0].message.content

system = BiospecimenRAGSystem()

@app.route('/api/query', methods=['POST'])
@limiter.limit("10 per minute")
def handle_query():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "Missing question"}), 400
            
        if not system.initialized:
            return jsonify({"error": "System initializing", "status": 503})
        
        start_time = time.time()
        
        # Check cache first
        cache_key = question.lower().strip()
        if cache_key in system.embeddings_cache:
            app.logger.info("Returning cached result")
            return jsonify(system.embeddings_cache[cache_key])
        
        embedding = system.generate_embeddings(question)
        results = system.query_kusto(embedding).collect()
        
        context = "\n".join([
            f"Document {idx+1} (Similarity: {row['similarity']:.2f}): {row['content']}"
            for idx, row in enumerate(results)
        ])
        
        answer = system.generate_response(question, context)
        
        response = {
            "answer": answer,
            "sources": [dict(row.asDict()) for row in results],
            "processing_time": f"{time.time() - start_time:.2f}s",
            "status": 200
        }
        
        # Cache result
        system.embeddings_cache[cache_key] = response
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Query failed: {str(e)}", exc_info=True)
        return jsonify({"error": str(e), "status": 500}), 500

@app.route('/api/status', methods=['GET'])
def status():
    try:
        test_query = system.query_kusto(system.generate_embeddings("test"), 1)
        return jsonify({
            "status": "ready" if system.initialized else "initializing",
            "records": test_query.count(),
            "version": "1.0.0"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)