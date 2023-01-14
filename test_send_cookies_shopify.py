import json
import os
from unittest.mock import patch
from dotenv import load_dotenv
from shopify import ShopifyResource, Session, Order
import pytest
from send_cookies_shopify import lambda_handler

@patch('shopify.Session')
def test_lambda_handler(mock_session):

    event = {
        "fbpCookie": "test_fbpCookie",
        "fbcCookie": "test_fbcCookie",
        "gclidCookie": "test_gclidCookie",
        "ttpCookie": "test_ttpCookie",
        "ttclidCookie": "test_ttclidCookie",
        "userAgent": "test_userAgent",
        "userIP": "test_userIP",
        "transaction_id": "5246318051611"
    }
    context = {}

    # Call lambda_handler
    lambda_handler(event, context)

    # Assert that the correct response is returned
    assert lambda_handler(event, context) == {
        'statusCode': 200,
        'body': json.dumps('Event data added to order note_attributes')
    }



