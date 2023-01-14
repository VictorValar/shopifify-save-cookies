import json
import os
from dotenv import load_dotenv
from shopify import ShopifyResource, Session, Order

# Load environment variables
load_dotenv()
SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')
SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION')
SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')

def lambda_handler(event, context):
    # Get event data
    fbpCookie = event["fbpCookie"]
    fbcCookie = event["fbcCookie"]
    gclidCookie = event["gclidCookie"]
    ttpCookie = event["ttpCookie"]
    ttclidCookie = event["ttclidCookie"]
    userAgent = event["userAgent"]
    userIP = event["userIP"]
    transaction_id = event["transaction_id"]

    # Create a new Shopify session
    session = Session(SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION, SHOPIFY_ACCESS_TOKEN)
    ShopifyResource.activate_session(session)

    # Get order using transaction_id
    order = Order.find(transaction_id)

    # Retrieve current note_attributes from the order
    current_note_attributes = order.note_attributes

    # Append event data to current order notes_attributes field
    current_note_attributes.append({
            "name": "fbpCookie",
            "value": fbpCookie
        })
    current_note_attributes.append({
            "name": "fbcCookie",
            "value": fbcCookie
        })
    current_note_attributes.append({
            "name": "gclidCookie",
            "value": gclidCookie
        })
    current_note_attributes.append({
            "name": "ttpCookie",
            "value": ttpCookie
        })
    current_note_attributes.append({
            "name": "ttclidCookie",
            "value": ttclidCookie
        })
    current_note_attributes.append({
            "name": "userAgent",
            "value": userAgent
        })
    current_note_attributes.append({
            "name": "userIP",
            "value": userIP
        })

    # Set the updated note_attributes to the order
    order.note_attributes = current_note_attributes

    # Update order
    order.save()
    return {
        'statusCode': 200,
        'body': json.dumps('Event data added to order note_attributes')
    }


if __name__ == "__main__":
    lambda_handler()