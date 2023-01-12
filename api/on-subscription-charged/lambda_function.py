import braintree
import os
import base64
import urllib.parse
import boto3
from datetime import datetime

def lambda_handler(event, context):
    request_body = urllib.parse.parse_qs(base64.b64decode(event["body"].encode()).decode())

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ["BRAINTREE_MERCHANT_ID"],
            public_key=os.environ["BRAINTREE_PUBLIC_KEY"],
            private_key=os.environ["BRAINTREE_PRIVATE_KEY"]
        )
    )

    webhook_notification = gateway.webhook_notification.parse(request_body["bt_signature"][0], request_body["bt_payload"][0])
    if webhook_notification.kind == "subscription_charged_successfully":
        # find customer and update their account
        payment_method = gateway.payment_method.find(webhook_notification.subject["subscription"]["payment_method_token"])

        period_end_date = webhook_notification.subject["subscription"]["billing_period_end_date"]
        period_end_timestamp = int(datetime(period_end_date.year, period_end_date.month, period_end_date.day).timestamp())

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.environ["ACCOUNTS_TABLE_NAME"])
        table.update_item(
            Key={
                "username": payment_method.customer_id,
            },
            UpdateExpression="SET subscription_status = :status, subscription_period_end_timestamp = :period_end_timestamp, subscription_id = :id",
            ExpressionAttributeValues={
                ":status": webhook_notification.subject["subscription"]["status"],
                ":period_end_timestamp": period_end_timestamp,
                ":id": webhook_notification.subject["subscription"]["id"],
            }
        )

    return { 
        "message": "Success",
    }