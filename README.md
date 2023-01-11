# Advanced Stream Stats

## Todo

- [x] Add skeleton layout
- [x] Add website hosting
- [x] Add sign in/out
- [x] Add account creation on sign in
- [ ] Add subscription check on page load
- [ ] Add one month and one year subscriptions
- [ ] Add cancel subscription

## Deploy
```
sam build
sam deploy --guided || sam deploy --guided --config-env prod
npm run build-dev || npm run build
aws s3 sync ./build s3://BUCKET-NAME --delete
aws cloudfront create-invalidation --distribution-id DISTRIBUTION-ID --paths "/*"
```
