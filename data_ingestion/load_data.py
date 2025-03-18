import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient

def upload_to_OneLake(file_path, lake_name, directory_name, file_name):
    """
    Upload data to OneLake.
    """
    service_client = DataLakeServiceClient.from_connection_string("<connection_string>")
    file_system_client = service_client.get_file_system_client(file_system=lake_name)
    directory_client = file_system_client.get_directory_client(directory_name)
    file_client = directory_client.create_file(file_name)
    
    with open(file_path, "rb") as data:
        file_client.append_data(data, offset=0, length=len(data))
        file_client.flush_data(len(data))
    
    print(f"Uploaded {file_name} to OneLake.")

# Example usage
upload_to_OneLake("data_ingestion/sample_data/genomic_data.csv", "genomics-lake", "raw-data", "genomic_data.csv")