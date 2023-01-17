import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')
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
    order_name = 'name:CLUBEGL' + event["order_name"]

    query = """
            query orders($order_name: String) {
                orders(query: $order_name, first: 1) {
                  edges {
                    node {
                      id
                      name
                      customAttributes { key value }
                    }
                  }
                }
            }
            """

    headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN}

    variables = {
        "order_name": order_name
        }

    data = {
        "query": query,
        "variables": variables
        }


    response = requests.post('https://gusttavolimastore.myshopify.com/admin/api/2023-01/graphql.json', json=data, headers=headers)

    result = response.json()

    # Catch errors in the result
    if 'errors' in result:
        raise Exception(result['errors'])

    # Check if the order exists
    if len(result["data"]["orders"]["edges"]) == 0:
        return {
            'statusCode': 404,
            'body': json.dumps('Order not found')
        }

    # Get the order ID and customAttributes from the query result
    order_id = result["data"]["orders"]["edges"][0]["node"]["id"]
    customAttributes = result["data"]["orders"]["edges"][0]["node"]["customAttributes"]

    # Append new customAttributes to the existing customAttributes
    customAttributes.append({"key": "fbpCookie", "value": fbpCookie})
    customAttributes.append({"key": "fbcCookie", "value": fbcCookie})
    customAttributes.append({"key": "gclidCookie", "value": gclidCookie})
    customAttributes.append({"key": "ttpCookie", "value": ttpCookie})
    customAttributes.append({"key": "ttclidCookie", "value": ttclidCookie})
    customAttributes.append({"key": "userAgent", "value": userAgent})
    customAttributes.append({"key": "userIP", "value": userIP})

    # Define the mutation query
    query = """
            mutation orderUpdate($order_id: ID!, $customAttributes: [AttributeInput!]!) {
                orderUpdate(input: {id:$order_id,customAttributes: $customAttributes}) {
                    order {
                        id
                        name
                        customAttributes { key value }
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
    # Execute the mutation
    headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN}

    variables = {
      "order_id": order_id.replace("'", ""),
      "customAttributes": customAttributes
    }
    data = {
      "query": query,
      "variables": variables
    }

    response = requests.post('https://gusttavolimastore.myshopify.com/admin/api/2023-01/graphql.json', json=data, headers=headers)

    result = response.json()

    # Check for errors in the mutation
    if 'errors' in result:
        raise Exception(result['errors'])

    return {
        'statusCode': 200,
        'body': json.dumps('Event data added to order customAttributes')
    }

if __name__ == "main":
    lambda_handler()



