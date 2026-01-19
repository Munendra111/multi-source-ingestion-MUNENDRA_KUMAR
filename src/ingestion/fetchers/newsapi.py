import os
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from ingestion.common import BaseFetcher, ArticleSchema

class NewsAPIFetcher(BaseFetcher):
    def __init__(self):
        self.api_key = os.getenv("NEWSAPI_API_KEY")
        self.session = requests.Session()
        # Resilience: Retry strategy for 429 and 500-level errors
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def fetch(self) -> list[ArticleSchema]:
        # 1. Check for API Key
        if not self.api_key:
            if "unittest" not in sys.modules:
                print("!!! NewsAPI Error: No API Key found in .env !!!")
            return []

        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": "technology", 
            "language": "en", 
            "apiKey": self.api_key, 
            "pageSize": 5
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            
            # 2. Check for unauthorized status
            if response.status_code == 401:
                if "unittest" not in sys.modules:
                    print("NewsAPI Error: Unauthorized. Please check your API Key.")
                return []
                
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("articles", []):
                articles.append(ArticleSchema(
                    title=item.get("title") or "No Title",
                    content=item.get("description") or "No Content",
                    source="newsapi",
                    url=item.get("url") or "N/A"
                ))
            
            # 3. Success Print (Silenced during tests)
            if "unittest" not in sys.modules:
                count = len(articles)
                unit = "article" if count == 1 else "articles"
                print(f"NewsAPI: Ingested {count} {unit} successfully.")
            
            return articles

        except Exception as e:
            # 4. Error Print (Silenced during tests)
            if "unittest" not in sys.modules:
                print(f"NewsAPI Exception: {e}")
            return []