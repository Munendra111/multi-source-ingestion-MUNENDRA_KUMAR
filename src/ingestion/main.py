import os
import json
import sys
from dotenv import load_dotenv

# --- THE PATH FIX ---
# Ensures 'src' is in the search path so we can use absolute package imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # src/ingestion
SRC_DIR = os.path.dirname(CURRENT_DIR)                  # src
PROJECT_ROOT = os.path.dirname(SRC_DIR)                 # celltron-ingestion

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Absolute imports from the ingestion package
from ingestion.fetchers.csv_reader import CSVFetcher
from ingestion.fetchers.newsapi import NewsAPIFetcher
from ingestion.fetchers.web_scraper import WebScraperFetcher

# Load API keys from the root .env file
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

def run_pipeline():
    """Orchestrates the fetching and saving of data from all sources."""
    
    # Silence start message during unit tests
    if "unittest" not in sys.modules:
        print("--- Celltron Ingestion Pipeline Starting ---")
    
    csv_path = os.path.join(PROJECT_ROOT, "data", "sample_data.csv")
    
    # Initialize fetchers
    sources = [
        CSVFetcher(csv_path),
        NewsAPIFetcher(),
        WebScraperFetcher("https://news.ycombinator.com/")
    ]

    final_data = []

    # Process each source
    for fetcher in sources:
        try:
            # Silence the "Executing" log during unit tests
            if "unittest" not in sys.modules:
                print(f"Executing: {fetcher.__class__.__name__}...")
                
            articles = fetcher.fetch()
            final_data.extend([a.model_dump() for a in articles])
        except Exception as e:
            if "unittest" not in sys.modules:
                print(f"Critical Error in {fetcher.__class__.__name__}: {e}")

    # Ensure output directory exists
    output_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save consolidated results to JSON
    output_file = os.path.join(output_dir, "articles.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    # Silence completion messages during unit tests
    if "unittest" not in sys.modules:
        print("-" * 45)
        print(f"SUCCESS: {len(final_data)} articles saved to {output_file}")
        print("--- Pipeline Execution Complete ---")

if __name__ == "__main__":
    run_pipeline()