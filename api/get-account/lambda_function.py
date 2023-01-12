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
    subscription_period_end_timestamp = account["subscription_period_end_timestamp"] if "subscription_period_end_timestamp" in account else 0
    subscription_status = account["subscription_status"] if "subscription_status" in account else ""

    return { 
        "message": "Success",
        "subscription_period_end_timestamp": subscription_period_end_timestamp,
        "subscription_status": subscription_status
    }