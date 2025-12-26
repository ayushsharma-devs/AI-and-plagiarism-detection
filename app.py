import os
import io
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from googleapiclient.discovery import build
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

# --- SECURE API KEY HANDLING ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
    try:
        from config import GOOGLE_API_KEY as G_KEY, SEARCH_ENGINE_ID as S_ID
        GOOGLE_API_KEY = GOOGLE_API_KEY or G_KEY
        SEARCH_ENGINE_ID = SEARCH_ENGINE_ID or S_ID
    except ImportError:
        print("Warning: Config file not found. Ensure Env Vars are set on Render.")

# --- NLTK PATH SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__))
nltk_data_dir = os.path.join(script_dir, "nltk_data")
nltk.data.path.insert(0, nltk_data_dir)

def google_search(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
    return res.get("items", [])

@app.route("/")
def index():
    return send_from_directory(script_dir, "index.html")

# NEW: Route to handle file uploads and extract text
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    extracted_text = ""
    try:
        if file.filename.endswith('.pdf'):
            reader = PdfReader(file)
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"
        elif file.filename.endswith('.txt'):
            extracted_text = file.read().decode('utf-8')
        else:
            return jsonify({"error": "Unsupported file type"}), 400
            
        return jsonify({"text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/check", methods=["POST"])
def check_plagiarism():
    data = request.json
    text_to_check = data.get("text", "")
    if not text_to_check:
        return jsonify({"error": "No text provided"}), 400

    sentences = sent_tokenize(text_to_check)
    matches = []

    for sentence in sentences:
        if len(sentence.split()) > 6: # Slightly stricter limit
            query = f'"{sentence}"' 
            try:
                results = google_search(query)
                if results:
                    matches.append({
                        "sentence": sentence,
                        "source": results[0].get("link"),
                        "title": results[0].get("title")
                    })
            except Exception as e:
                print(f"Search error: {e}")

    return jsonify({"matches": matches})

if __name__ == "__main__":
    app.run(debug=True, port=5000)