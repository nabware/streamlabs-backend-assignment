# Advanced Stream Stats

## Todo

- [x] Add skeleton layout
- [x] Add website hosting
- [x] Add sign in/out
- [ ] Add account creation on sign in
- [ ] Add account check on page load

## Deploy
```
sam build
sam deploy --guided || sam deploy --guided --config-env prod
npm run build-dev || npm run build
aws s3 sync ./build s3://BUCKET-NAME --delete
aws cloudfront create-invalidation --distribution-id DISTRIBUTION-ID --paths "/*"
```
