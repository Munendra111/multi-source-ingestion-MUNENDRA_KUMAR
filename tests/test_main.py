import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ingestion.main import run_pipeline

class TestMainOrchestration(unittest.TestCase):
    def test_pipeline_execution(self):
        """Tests if the main function runs and creates output files."""
        # We run the pipeline (this will use real data if available)
        run_pipeline()
        
        # Check if the output directory and file were created
        output_file = "output/articles.json"
        self.assertTrue(os.path.exists(output_file))
        
        # Check if JSON is valid
        with open(output_file, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()