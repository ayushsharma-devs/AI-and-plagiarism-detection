AI Plagiarism Guard
AI Plagiarism Guard is a web-based utility designed to verify content integrity by performing web-scale analysis using the Google Custom Search API. It allows users to input text directly or upload documents to identify potential matches across the internet.
The service can be accessed through this link : https://ai-and-plagiarism-detection.onrender.com
Features
Text Analysis: Scans input text by tokenizing it into sentences and checking for exact matches online.

File Upload Support: Extracts and analyzes text from .pdf and .txt files.

Real-time Results: Provides a list of potential matches, including the specific sentence found, the source title, and a direct link to the original content.

Clean UI: A responsive, "glassmorphism" styled interface built with Tailwind CSS.

Tech Stack
Backend: Flask (Python)

Frontend: HTML5, Tailwind CSS, JavaScript

Search Engine: Google Custom Search API

NLP: NLTK (Natural Language Toolkit) for sentence tokenization

Deployment: Ready for platforms like Render or Heroku via Gunicorn.

Installation & Setup
1. Prerequisites
Ensure you have Python installed and a Google Cloud Project with the Custom Search API enabled. You will need:

GOOGLE_API_KEY

SEARCH_ENGINE_ID (CX)

2. Clone and Install Dependencies
Bash

pip install -r requirements.txt
The dependencies include Flask, Gunicorn, NLTK, Google API Python Client, and PyPDF2.

3. NLTK Data Setup
The application requires the punkt tokenizer. Run the provided helper script to download it locally to the project directory:

Bash

python download_nltk.py
This script ensures the data is stored in an nltk_data folder within your project for deployment compatibility.

4. Configuration
You can configure your credentials in two ways:

Environment Variables: Set GOOGLE_API_KEY and SEARCH_ENGINE_ID in your environment.

Config File: Create a config.py (which is ignored by git) and add your keys:

Python

GOOGLE_API_KEY = "your_key_here"
SEARCH_ENGINE_ID = "your_search_engine_id_here"
Usage
Start the Server:

Bash

python app.py
Access the App: Open your browser and navigate to http://127.0.0.1:5000.

Analyze: Paste text into the text area or drag and drop a supported file into the upload zone.

Review: Click "Analyze Content" to view potential plagiarism matches.

License
This project is licensed under the MIT License.
