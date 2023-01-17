import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')
SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')

def options_handler(event, context):
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }
    return response

def main_handler(event, context):

    print('EVENT:', event)
    # Get event data
    fbpCookie = event["fbpCookie"] if event["fbpCookie"] else None
    fbcCookie = event["fbcCookie"] if event["fbpCookie"] else None
    gclidCookie = event["gclidCookie"] if event["fbpCookie"] else None
    ttpCookie = event["ttpCookie"] if event["fbpCookie"] else None
    ttclidCookie = event["ttclidCookie"] if event["fbpCookie"] else None
    userAgent = event["userAgent"] if event["fbpCookie"] else None
    userIP = event["userIP"] if event["fbpCookie"] else None
    order_name = 'name:CLUBEGL' + event["order_name"].replace("#", "")

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


    response = requests.post(f'https://{SHOPIFY_SHOP_URL}/admin/api/2023-01/graphql.json', json=data, headers=headers)

    result = response.json()

    # Catch errors in the result
    if 'errors' in result:
        raise Exception(result['errors'])

    # Check if the order exists
    if len(result["data"]["orders"]["edges"]) == 0:
        return {
            'statusCode': 404,
            'body': json.dumps('Order not found'),
            'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
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

    response = requests.post(f'https://{SHOPIFY_SHOP_URL}/admin/api/2023-01/graphql.json', json=data, headers=headers)

    result = response.json()

    # Check for errors in the mutation
    if 'errors' in result:
        raise Exception(result['errors'])

    return {
        'statusCode': 200,
        'body': json.dumps('Event data added to order customAttributes'),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }

def lambda_handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return options_handler(event, context)
    else:
        return main_handler(event, context)




