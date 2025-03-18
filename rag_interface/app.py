from flask import Flask, request, jsonify, render_template
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

app = Flask(__name__)

def generate_response(prompt):
    """
    Generate a response using Azure OpenAI.
    """
    client = AzureOpenAI(api_key="<api_key>", api_version="2023-05-15", azure_endpoint="https://<resource-name>.openai.azure.com")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle chat requests.
    """
    user_input = request.json.get("message")
    
    # Retrieve relevant documents from Azure AI Search
    endpoint = "https://my-search-service.search.windows.net"
    credential = AzureKeyCredential("<api_key>")
    client = SearchClient(endpoint=endpoint, index_name="genomics-index", credential=credential)
    
    results = client.search(search_text=user_input)
    context = " ".join([result["content"] for result in results])
    
    # Generate response using Azure OpenAI
    prompt = f"Context: {context}\n\nQuestion: {user_input}\n\nAnswer:"
    response = generate_response(prompt)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)