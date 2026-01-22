#!/bin/bash

echo "Starting deployment..."

# Deploy Cloud Functions
echo "Deploying Cloud Functions..."
cd cloud_functions/send_order_email
gcloud functions deploy send-order-email \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --entry-point send_order_email

cd ../recommend_games
gcloud functions deploy recommend-games \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --entry-point recommend_games

# Deploy App Engine
echo "Deploying to App Engine..."
cd ../..
gcloud app deploy --quiet

echo "Deployment complete!"