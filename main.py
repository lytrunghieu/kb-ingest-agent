import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from src.scraper import scrape_articles, load_state, save_state

# Setup
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in environment.")
    exit(1)

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply."""

def upload_to_gemini(filepath):
    print(f"Uploading {filepath} to Gemini...")
    uploaded_file = genai.upload_file(path=filepath, mime_type="text/plain")
    # Wait briefly to let the file process
    while uploaded_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        uploaded_file = genai.get_file(uploaded_file.name)
    print(" Done!")
    return uploaded_file.name

def main():
    print("Starting Job...")
    # Step 1: Run scraper to get delta
    results = scrape_articles()
    
    new_files = results["new"]
    updated_files = results["updated"]
    
    files_to_upload = new_files + updated_files
    
    state = load_state()
    gemini_files = state.get("gemini_files", {})
    
    uploaded_count = 0
    # Step 2: Upload delta to Gemini
    for filepath in files_to_upload:
        filename = os.path.basename(filepath)
        
        # If this is an update, we could optionally delete the old file from Gemini first
        old_uri = gemini_files.get(filename)
        if old_uri:
            try:
                genai.delete_file(old_uri)
                print(f"Deleted old version of {filename} from Gemini.")
            except Exception as e:
                print(f"Could not delete old file {old_uri}: {e}")
                
        new_uri = upload_to_gemini(filepath)
        gemini_files[filename] = new_uri
        uploaded_count += 1
        
    state["gemini_files"] = gemini_files
    save_state(state)
    
    print(f"Gemini Upload Complete. Embedded {uploaded_count} new/updated files (Chunks: 1 per file due to high context window).")
    
    # Quick Sanity Check Mode (Only run if manually testing)
    if os.environ.get("RUN_SANITY_CHECK") == "true":
        print("\n--- Running Sanity Check ---")
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT
        )
        
        # Load all available files into a single user turn
        valid_file_parts = []
        for name, uri in gemini_files.items():
            try:
                gfile = genai.get_file(uri)
                valid_file_parts.append(gfile)
            except Exception:
                pass # skip if expired
                
        history = [
            {
                "role": "user",
                "parts": valid_file_parts + ["I have uploaded the knowledge base. Please acknowledge."]
            },
            {
                "role": "model",
                "parts": ["Acknowledged. I am OptiBot. How can I help you?"]
            }
        ]
        
        chat = model.start_chat(history=history)
        response = chat.send_message("How do I add a YouTube video?")
        print(f"Bot: {response.text}")

if __name__ == "__main__":
    main()
