from openai import AzureOpenAI
import pandas as pd

def generate_report(data_path):
    """
    Generate a report using Azure OpenAI.
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Summarize data
    summary = df.describe().to_string()
    
    # Generate insights using Azure OpenAI
    client = AzureOpenAI(api_key="<api_key>", api_version="2023-05-15", azure_endpoint="https://<resource-name>.openai.azure.com")
    prompt = f"Summarize the following data and provide key insights:\n\n{summary}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    insights = response.choices[0].message.content
    
    # Save report
    with open("report.txt", "w") as f:
        f.write(insights)
    print("Report generated and saved to report.txt.")

# Example usage
generate_report("data_ingestion/sample_data/genomic_data.csv")