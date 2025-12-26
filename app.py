# Install these first!
# pip install Flask flask-cors nltk google-api-python-client
import os
from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from googleapiclient.discovery import build
import nltk

nltk.download('punkt_tab')

script_dir = os.path.dirname(os.path.abspath(__file__))
nltk_data_dir = os.path.join(script_dir, "nltk_data")
nltk.data.path.insert(0, nltk_data_dir)
# ----------------------
# Download the NLTK sentence splitter (only need to do this once)
# You can run this part in a separate python shell first
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize

app = Flask(__name__)
CORS(app)  # Allows your frontend to talk to this backend

# --- PUT YOUR KEYS HERE ---
GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID= os.getenv("SEARCH_ENGINE_ID")

if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
    try:
        from config import GOOGLE_API_KEY as G_KEY, SEARCH_ENGINE_ID as S_ID
        GOOGLE_API_KEY = GOOGLE_API_KEY or G_KEY
        SEARCH_ENGINE_ID = SEARCH_ENGINE_ID or S_ID
    except ImportError:
        print("Warning: API keys not found in Environment or config.py")
# --------------------------

# Build the Google Custom Search service
def google_search(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
    return res.get("items", [])
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")
@app.route("/check", methods=["POST"])
def check_plagiarism():
    data = request.json
    text_to_check = data.get("text", "")

    if not text_to_check:
        return jsonify({"error": "No text provided"}), 400

    # Split the text into sentences
    sentences = sent_tokenize(text_to_check)
    matches = []

    print(f"Checking {len(sentences)} sentences...")

    for sentence in sentences:
        # We only check sentences of a reasonable length
        if len(sentence.split()) > 5:  # e.g., ignore "Hello."
            
            # This is the "hack": search for the *exact* sentence in quotes
            query = f'"{sentence}"' 
            
            try:
                results = google_search(query)
                if results:
                    # If we got any result, it's a match
                    first_result = results[0]
                    matches.append({
                        "sentence": sentence,
                        "source": first_result.get("link"),
                        "title": first_result.get("title")
                    })
                    print(f"Found match: {sentence}")
                    
            except Exception as e:
                print(f"Error searching for sentence: {e}")

    # Return the list of all matched sentences and their sources
    return jsonify({"matches": matches})

if __name__ == "__main__":
    # Make sure NLTK data is available IN OUR CUSTOM PATH
    try:
        # We explicitly tell find() to look in our path
        nltk.data.find('tokenizers/punkt', paths=[nltk_data_dir])
        print("NLTK 'punkt' tokenizer found locally.")
    except LookupError:
        print(f"--- ERROR ---")
        print(f"NLTK 'punkt' tokenizer not found in {nltk_data_dir}.")
        print("Please run the `python download_nltk.py` script first.")
        print("---------------")
        exit() # Stop the server from running
        
    app.run(debug=True, port=5000)