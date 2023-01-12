import braintree
import os
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    request_body = json.loads(event["body"])
    payment_method_nonce = request_body["payment_method_nonce"]
    plan_id = os.environ["TWELVE_MONTH_SUBSCRIPTION_PLAN_ID"] if request_body["months"] == 12 else os.environ["ONE_MONTH_SUBSCRIPTION_PLAN_ID"]

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ["BRAINTREE_MERCHANT_ID"],
            public_key=os.environ["BRAINTREE_PUBLIC_KEY"],
            private_key=os.environ["BRAINTREE_PRIVATE_KEY"]
        )
    )

    # create subscription and update account
    result = gateway.subscription.create({
        "payment_method_nonce": payment_method_nonce,
        "plan_id": plan_id,
    })

    payment_method = gateway.payment_method.find(result.subscription.payment_method_token)

    period_end_date = result.subscription.billing_period_end_date
    period_end_timestamp = int(datetime(period_end_date.year, period_end_date.month, period_end_date.day).timestamp())

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ACCOUNTS_TABLE_NAME"])
    table.update_item(
        Key={
            "username": payment_method.customer_id,
        },
        UpdateExpression="SET subscription_status = :status, subscription_period_end_timestamp = :period_end_timestamp, subscription_id = :id",
        ExpressionAttributeValues={
            ":status": result.subscription.status,
            ":period_end_timestamp": period_end_timestamp,
            ":id": result.subscription.id,
        }
    )

    return { 
        "message": "Success",
    }