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

    print('EVENT:', event.get('body'))
    event = json.loads(event.get('body'))
    print('EVENTTYPE:', type(event.get('body')))
    # Get event data
    fbpCookie = event.get("fbpCookie")
    fbcCookie = event.get("fbcCookie")
    gclidCookie = event.get("gclidCookie")
    ttpCookie = event.get("ttpCookie")
    ttclidCookie = event.get("ttclidCookie")
    userAgent = event.get("userAgent")
    userIP = event.get("userIP")
    order_name = 'name:CLUBEGL' + event.get("transaction_id")

    # Return 400 if any transaction_id is not found or is empty
    if not event.get("transaction_id"):
        print('TRANSACTION ID NOT FOUND')
        return {
            'statusCode': 400,
            'body': json.dumps('TRANSACTION ID NOT FOUND'),
            'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        }


    print('ORDER NAME:', order_name)


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

    print('QUERY:', query)

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
    print('MUTATION:', query)
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




