import os
from dotenv import load_dotenv
from notebookutils import mssparkutils

load_dotenv()

class Config:
    # Environment fallback for local development vs Fabric
    def _get_config_value(self, env_name, scope=None, secret_name=None):
        val = os.getenv(env_name)
        if val:
            return val
        if scope and secret_name:
            try:
                return mssparkutils.credentials.getSecret(scope, secret_name)
            except:
                pass
        return None

    # Azure OpenAI
    OPENAI_ENDPOINT = _get_config_value('OPENAI_ENDPOINT', 'openai-scope', 'OPENAI_ENDPOINT')
    OPENAI_KEY = _get_config_value('OPENAI_KEY', 'openai-scope', 'OPENAI_KEY')
    OPENAI_API_VERSION = "2023-09-01-preview"
    OPENAI_GPT4_DEPLOYMENT = "gpt-4"
    OPENAI_EMBEDDING_DEPLOYMENT = "text-embedding-ada-002"
    
    # Kusto/Eventhouse
    KUSTO_URI = _get_config_value('KUSTO_URI', None, None) or "https://trd-zdxwqrcu1znbqygpxg.z2.kusto.fabric.microsoft.com"
    KUSTO_DB = _get_config_value('KUSTO_DB', None, None) or "BioEventHouse"
    KUSTO_TABLE = "biospecimen_embeddings"
    
    # Monitoring
    APP_INSIGHTS_KEY = _get_config_value('APP_INSIGHTS_KEY', 'monitoring-scope', 'APP_INSIGHTS_KEY')
    
    # Security
    SECRET_KEY = _get_config_value('SECRET_KEY', None, None)
    RATE_LIMIT = "100 per day, 10 per minute"
    
    # Data paths
    DATA_PATH = "/lakehouse/default/Files/biospecimen_data.csv"