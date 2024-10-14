import unittest
from unittest.mock import patch
from api.requests import get_wikipedia_article


class TestWikipediaArticleRetrieval(unittest.TestCase):

    @patch("requests.get")
    def test_successful_article_retrieval(self, mock_get):
        mock_response = {
            "query": {
                "pages": {
                    "123": {
                        "extract": "This is a test article."
                    }
                }
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_wikipedia_article("Test Article")

        self.assertEqual(result, "This is a test article.")

    @patch("requests.get")
    def test_article_not_found(self, mock_get):
        mock_response = {
            "query": {
                "pages": {
                    "0": {
                        "missing": ""
                    }
                }
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_wikipedia_article("Nonexistent Article")

        self.assertEqual(result, "Article not found.")

    @patch("requests.get")
    def test_request_error(self, mock_get):
        mock_get.return_value.status_code = 500
        result = get_wikipedia_article("Test Article")

        self.assertEqual(result, "Error: 500")
