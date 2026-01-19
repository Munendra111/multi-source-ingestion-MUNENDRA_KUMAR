import unittest
import os
import sys

# Ensure 'src' is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ingestion.fetchers.csv_reader import CSVFetcher

class TestCSVFetcher(unittest.TestCase):
    def setUp(self):
        self.test_csv = "tests/test_sample.csv"
        with open(self.test_csv, "w") as f:
            f.write("headline,body\nTest Headline,Test Body")

    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_fetch_valid_csv(self):
        fetcher = CSVFetcher(self.test_csv)
        articles = fetcher.fetch()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test Headline")

    def test_file_not_found(self):
        fetcher = CSVFetcher("non_existent.csv")
        articles = fetcher.fetch()
        self.assertEqual(articles, [])