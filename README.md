# Advanced Stream Stats

Live demo: https://d3qn2m39g873t3.cloudfront.net/

Braintree valid card numbers: https://developer.paypal.com/braintree/docs/guides/credit-cards/testing-go-live/python#valid-card-numbers

[![Watch the video](https://img.youtube.com/vi/oY5fhAE6rd4/default.jpg)](https://youtu.be/oY5fhAE6rd4)

## Todo

- [x] Add skeleton layout
- [x] Add website hosting
- [x] Add sign in/out
- [x] Add account creation on sign in
- [x] Add subscription check on page load
- [x] Add monthly and yearly subscriptions
- [x] Add cancel subscription

## Deploy

```
sam build
sam deploy --guided || sam deploy --guided --config-env prod
npm run build-dev || npm run build
aws s3 sync ./build s3://BUCKET-NAME --delete
aws cloudfront create-invalidation --distribution-id DISTRIBUTION-ID --paths "/*"
```

## Stack

- Python on Lambda (Serverless)
- TypeScript with SvelteKit
- NoSQL with DynamoDB
- CloudFront CDN
- Cognito (Login system)

## Issues

If you resubscribe to the same type of subscription (monthly, yearly) shortly after canceling you will receive a duplication error.
```
<ErrorResult 'Gateway Rejected: duplicate' at ffffa61bfa60>
```