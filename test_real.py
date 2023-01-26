import unittest
import os
import json
from dotenv import load_dotenv
from send_cookies_shopify import main_handler

class TestLambdaHandlerWithRealData(unittest.TestCase):

    def setUp(self):
        # Load environment variables
        load_dotenv()
        self.SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')
        self.SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')

    def test_main_handler_with_real_data(self):
        # Define test event data
        event = {
            "fbpCookie": "mock_fbpCookie",
            "fbcCookie": "mock_fbcCookie",
            "gclidCookie": "mock_gclidCookie",
            "ttpCookie": "mock_ttpCookie",
            "ttclidCookie": "mock_ttclidCookie",
            "userIP": "mock_userIP",
            "transaction_id": "4207"
        }

        # Call the main_handler function
        # event = json.dumps(event)
        result = main_handler(event, None)

        # Assert that the function returned a status code of 200
        self.assertEqual(result['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()