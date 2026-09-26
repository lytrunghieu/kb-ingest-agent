import os
import requests
import json
from markdownify import markdownify as md

API_URL = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sync_state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_run_timestamp": "2000-01-01T00:00:00Z", "gemini_files": {}}

def save_state(state_dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state_dict, f, indent=4)

def scrape_articles():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    state = load_state()
    last_run_timestamp = state.get("last_run_timestamp", "2000-01-01T00:00:00Z")
    
    print(f"Fetching articles from {API_URL}...")
    response = requests.get(API_URL)
    response.raise_for_status()
    
    data = response.json()
    articles = data.get("articles", [])
    
    print(f"Found {len(articles)} articles.")
    
    new_files = []
    updated_files = []
    skipped_count = 0
    
    max_updated_at = last_run_timestamp

    for article in articles:
        article_id = article.get("id")
        title = article.get("title", "Untitled")
        body = article.get("body", "")
        updated_at = article.get("updated_at", "")
        url = article.get("html_url", "")
        
        if not body:
            continue
            
        # Delta logic: skip if not updated since last run
        if updated_at <= last_run_timestamp:
            skipped_count += 1
            continue
            
        if updated_at > max_updated_at:
            max_updated_at = updated_at

        # Create slug
        slug = "".join(c if c.isalnum() else "-" for c in title).strip("-").lower()
        import re
        slug = re.sub(r'-+', '-', slug)
        
        filename = f"{article_id}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        is_update = os.path.exists(filepath)
        
        # Convert HTML to Markdown
        markdown_content = md(body, heading_style="ATX")
        # Add metadata for the AI to reference the URL
        final_content = f"# {title}\n\nArticle URL: {url}\n\n{markdown_content}"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        if is_update:
            updated_files.append(filepath)
        else:
            new_files.append(filepath)
            
    # Save the latest timestamp we saw
    state["last_run_timestamp"] = max_updated_at
    save_state(state)
    print(f"Scrape complete. New: {len(new_files)}, Updated: {len(updated_files)}, Skipped: {skipped_count}.")
    
    return {
        "new": new_files,
        "updated": updated_files,
        "skipped_count": skipped_count
    }

if __name__ == "__main__":
    scrape_articles()
