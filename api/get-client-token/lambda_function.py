import braintree
import os

def lambda_handler(event, context):
    username = event["headers"]["authorization"]

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ["BRAINTREE_MERCHANT_ID"],
            public_key=os.environ["BRAINTREE_PUBLIC_KEY"],
            private_key=os.environ["BRAINTREE_PRIVATE_KEY"]
        )
    )

    client_token = gateway.client_token.generate({
        "customer_id": username
    })

    return { 
        "message": "Success",
        "client_token": client_token,
    }