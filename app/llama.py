import requests
import os

# Load the Hugging Face token from environment variable
HF_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

def generate_summary(content: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": content,
        "options": {"use_cache": False}
    }
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct"

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("generated_text", "No summary generated")
    else:
        return f"Error: {response.status_code} - {response.text}"
