from flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS  

app = Flask(__name__, static_folder="static", template_folder="templates")  # Ensure correct folders
CORS(app)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}

def query_huggingface(prompt):
    """Send request to Hugging Face API and return the response"""
    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=data)
    return response.json()

# ✅ Serve the frontend (index.html)
@app.route('/')
def home():
    return render_template("index.html")  # Loads your frontend

@app.route('/query', methods=['POST'])
def query_model():
    """Flask API endpoint to process user queries"""
    data = request.json
    query_type = data.get("query_type")
    input_text = data.get("input_text")

    if not input_text:
        return jsonify({"error": "No input provided"}), 400

    if query_type == "disease":
        prompt = f"What are the symptoms, prevention, cure, and recommended food & activities for {input_text}?"
    elif query_type == "condition":
        prompt = f"What could be the possible causes, tests, and solutions for {input_text}?"
    else:
        return jsonify({"error": "Invalid query type"}), 400

    result = query_huggingface(prompt)
    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
