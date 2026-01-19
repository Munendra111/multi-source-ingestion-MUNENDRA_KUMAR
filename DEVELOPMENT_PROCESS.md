# Development Process: Multi-Source Data Ingestion Pipeline

## 1. Problem Understanding
The task was to build a Python-based ingestion system capable of fetching news/article data from three distinct sources:

* **NewsAPI** (REST API)
* **Local CSV** (File System)
* **Hacker News** (Web Scraper)

The core challenge was **Normalization**: ensuring that data from a structured API, a semi-structured CSV, and unstructured HTML all mapped to a single, consistent JSON schema.

## 2. Technical Breakdown & Workflow
I followed an "AI-Assisted Philosophy" by breaking the project into small, manageable tasks:

* **Task 1: Foundation.** Defined a `BaseFetcher` abstract class and an `ArticleSchema` using **Pydantic** for strict data validation and timezone-aware timestamps.
* **Task 2: Local Data.** Built the `CSVFetcher` to handle local files and manage missing fields with professional pluralization logic.
* **Task 3: API Integration.** Built the `NewsAPIFetcher` with a focus on network resilience using a `urllib3` **Retry strategy** for 429 and 500 status codes.
* **Task 4: Web Extraction.** Developed a `WebScraperFetcher` using **BeautifulSoup** with custom headers and length-based headline filtering.
* **Task 5: Orchestration.** Created `main.py` to stitch components together, ensuring the system remains portable across environments.



## 3. AI Prompts & Iterative Development
I used AI (Gemini) to generate the initial scaffold while maintaining control over the execution. Key prompts included:

* *"Create a Python Pydantic model for an article with title, content, source, and fetched_at fields using timezone-aware UTC."*
* *"Write a Python NewsAPI client using the requests library that implements a Retry strategy for 429 and 500 status codes."*
* *"Write a BeautifulSoup scraper that extracts headlines from Hacker News and maps them to a specific schema."*

## 4. Critical Review & Debugging (Ownership)
This was the most important phase. I resolved several critical issues to make the code production-ready:

* **Module Resolution:** Fixed `ModuleNotFoundError` by transitioning from relative imports to absolute package imports (`ingestion.common`). I implemented path injection logic in `main.py` and test files to ensure the module is portable.
* **Test Environment Silencing:** I identified that internal logs were cluttering the unit test output. I implemented a `sys.modules` check to silence fetcher prints during testing, resulting in a clean **"dots-only"** test result while maintaining verbose logs for manual execution.
* **Scraper Resilience:** Refined the initial AI scraper logic to look for broader anchor tags and added a `User-Agent` header to prevent being blocked by server-side bot detection.

## 5. Trade-offs & Decisions
* **Pydantic:** Chosen over simple dictionaries to catch "dirty data" early and enforce type safety.
* **Absolute Pathing:** Used in `main.py` to make the system easier to run regardless of the user's current working directory.
* **Mocking in Tests:** Chose to mock API and Scraper responses in unit tests using `unittest.mock` to ensure the test suite is fast, reliable, and does not require active internet or API keys to pass.

## 6. How to Run
1.  **Install dependencies:** `pip install -r requirements.txt`
2.  **Add your API Key:** Place your `NEWSAPI_API_KEY` in a `.env` file in the root directory.
3.  **Run the pipeline:** `python src/ingestion/main.py`
4.  **Run unit tests:** `python -m unittest discover tests`