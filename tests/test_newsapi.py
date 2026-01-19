import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ingestion.fetchers.newsapi import NewsAPIFetcher

class TestNewsAPIFetcher(unittest.TestCase):
    @patch('ingestion.fetchers.newsapi.requests.Session.get')
    def test_fetch_success(self, mock_get):
        # Simulate a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "articles": [{"title": "AI News", "description": "AI is growing", "url": "http://test.com"}]
        }
        mock_get.return_value = mock_response

        fetcher = NewsAPIFetcher()
        fetcher.api_key = "fake_key" # Force a key for testing
        articles = fetcher.fetch()
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "AI News")

    def test_no_key_handling(self):
        fetcher = NewsAPIFetcher()
        fetcher.api_key = None
        articles = fetcher.fetch()
        self.assertEqual(articles, [])