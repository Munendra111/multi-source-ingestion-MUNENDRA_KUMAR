import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ingestion.fetchers.web_scraper import WebScraperFetcher

class TestWebScraperFetcher(unittest.TestCase):
    @patch('ingestion.fetchers.web_scraper.requests.get')
    def test_fetch_html_parsing(self, mock_get):
        # Simulate HTML content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <a href="https://test.com/1">This is a very long title for a news article that exceeds twenty five characters</a>
            <a href="/relative/path">Another very long headline for testing purposes today</a>
        </html>
        """
        mock_get.return_value = mock_response

        fetcher = WebScraperFetcher("https://news.ycombinator.com/")
        articles = fetcher.fetch()
        
        # Check if scraper found articles and handled relative URL
        self.assertTrue(len(articles) >= 1)
        self.assertIn("https://news.ycombinator.com", articles[1].url)

    def test_scraper_failure(self,):
        with patch('ingestion.fetchers.web_scraper.requests.get', side_effect=Exception("Connection Error")):
            fetcher = WebScraperFetcher("http://invalid.url")
            articles = fetcher.fetch()
            self.assertEqual(articles, [])