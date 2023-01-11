import boto3
import os

def lambda_handler(event, context):
    username = event["headers"]["authorization"]

    # get account
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ACCOUNTS_TABLE_NAME"])
    account_response = table.get_item(
        Key={
            "username": username,
        }
    )

    account = account_response["Item"]
    subscription_period_end_date = account["subscription_period_end_date"] if "subscription_period_end_date" in account else 0
    subscription_status = account["subscription_status"] if "subscription_status" in account else "expired"

    return { 
        "message": "Success",
        "subscription_period_end_date": subscription_period_end_date,
        "subscription_status": subscription_status
    }