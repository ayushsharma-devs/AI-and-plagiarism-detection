import nltk
import os

# Define the directory *inside* your project
# os.path.abspath(__file__) gets the full path of the script
# os.path.dirname(...) gets the directory that script is in
script_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(script_dir, "nltk_data")

# Create the directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

print(f"Downloading NLTK data to: {download_dir}")

# Tell NLTK to download 'punkt' to that specific directory
nltk.download('punkt', download_dir=download_dir)

# Some search results suggest 'punkt_tab' can be downloaded separately
# if 'punkt' fails. Let's try it just in case.
try:
    nltk.download('punkt_tab', download_dir=download_dir)
except Exception as e:
    print(f"Could not download 'punkt_tab' (this is usually fine): {e}")

print("Download complete. You can now run app.py")