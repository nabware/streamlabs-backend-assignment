import os
import requests
import base64
import json
import boto3
import braintree

def lambda_handler(event, context):
    request_body = json.loads(event["body"])

    data = {"code": request_body["code"], 
    "code_verifier": request_body["code_verifier"], 
    "redirect_uri": request_body["redirect_uri"], 
    "client_id": os.environ["COGNITO_CLIENT_ID"], 
    "grant_type": "authorization_code"}

    client_id_secret = os.environ["COGNITO_CLIENT_ID"] + ":" + os.environ["COGNITO_CLIENT_SECRET"]
    client_secret_encoded = base64.b64encode(client_id_secret.encode()).decode()

    # exchange code for user info
    token_response = requests.post(os.environ["COGNITO_URL"] + "/oauth2/token", headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + client_secret_encoded}, data=data)
    tokens = token_response.json()
    user_info_response = requests.post(os.environ["COGNITO_URL"] + "/oauth2/userInfo", headers={"Authorization": "Bearer " + tokens["access_token"]})
    user_info = user_info_response.json()

    # get account
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ACCOUNTS_TABLE_NAME"])
    account_response = table.get_item(
        Key={
            "username": user_info["username"],
        }
    )
    
    if not "Item" in account_response:
        # create Braintree customer
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=os.environ["BRAINTREE_MERCHANT_ID"],
                public_key=os.environ["BRAINTREE_PUBLIC_KEY"],
                private_key=os.environ["BRAINTREE_PRIVATE_KEY"]
            )
        )

        gateway.customer.create({
            "id": user_info["username"],
            "email": user_info["email"],
            "first_name": user_info["given_name"],
            "last_name": user_info["family_name"],
        })

        # create new account
        table.put_item(
            Item={
                    "username": user_info["username"],
                    "email": user_info["email"],
                    "given_name": user_info["given_name"],
                    "family_name": user_info["family_name"],
                }
            )

    return { 
        "message": "Success",
        "username": user_info["username"],
    }