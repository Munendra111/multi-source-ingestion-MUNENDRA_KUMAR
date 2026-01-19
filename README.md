# Multi-Source Data Ingestion Pipeline

A Python-based system to fetch, normalize, and consolidate news data from REST APIs, CSV files, and Web Scrapers into a unified JSON schema.

## Features
- **Strict Validation**: Uses Pydantic for data normalization.
- **Resilience**: Implements Retry strategies for API calls.
- **Portability**: Uses absolute pathing for reliable execution.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `NEWSAPI_API_KEY` to a `.env` file.
4. Run the pipeline: `python src/ingestion/main.py`
5. Run tests: `python -m unittest discover tests`