import braintree
import os
import boto3

def lambda_handler(event, context):
    username = event["headers"]["authorization"]

    # get account for the subscription id
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ACCOUNTS_TABLE_NAME"])
    account_response = table.get_item(
        Key={
            "username": username,
        }
    )

    account = account_response["Item"]

    # cancel subscription
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ["BRAINTREE_MERCHANT_ID"],
            public_key=os.environ["BRAINTREE_PUBLIC_KEY"],
            private_key=os.environ["BRAINTREE_PRIVATE_KEY"]
        )
    )

    result = gateway.subscription.cancel(account["subscription_id"])

    # update account subscription status
    table.update_item(
        Key={
            "username": username,
        },
        UpdateExpression="SET subscription_status = :status",
        ExpressionAttributeValues={
            ":status": result.subscription.status,
        }
    )

    return { 
        "message": "Success",
        "subscription_status": result.subscription.status,
    }