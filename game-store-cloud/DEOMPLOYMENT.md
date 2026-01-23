# Deployment Guide

## Prerequisites
- Google Cloud Project created
- Cloud SQL instance running
- Firestore database created
- gcloud CLI authenticated

## Cloud Functions Deployment

### Email Notification Function
```bash
cd cloud_functions/send_order_email
gcloud functions deploy send-order-email \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --entry-point send_order_email
```

### Game Recommendation Function
```bash
cd cloud_functions/recommend_games
gcloud functions deploy recommend-games \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --entry-point recommend_games
```

## App Engine Deployment

### First Time Setup
```bash
gcloud app create --region=europe-west2
```

### Deploy Application
```bash
gcloud app deploy
```

### View Deployed App
```bash
gcloud app browse
```

## Configuration

### Environment Variables
Set in `app.yaml`:
- `SECRET_KEY`: Flask secret key for sessions
- `GCP_PROJECT_ID`: Your Google Cloud project ID
- `CLOUD_SQL_CONNECTION_NAME`: Cloud SQL connection string
- `DB_NAME`: Database name (gamestore)
- `DB_USER`: Database user (postgres)
- `DB_PASSWORD`: Database password

### Cloud SQL Connection
The app connects to Cloud SQL using the built-in App Engine service account.

## Monitoring

### View Logs
```bash
# Application logs
gcloud app logs tail -s default

# Cloud Function logs
gcloud functions logs read FUNCTION_NAME --region=europe-west2
```

### Cloud Console
- App Engine: https://console.cloud.google.com/appengine
- Cloud Functions: https://console.cloud.google.com/functions
- Cloud SQL: https://console.cloud.google.com/sql

## Troubleshooting

### Database Connection Issues
1. Verify Cloud SQL instance is running
2. Check connection name in app.yaml
3. Verify database credentials
4. Check Cloud SQL Admin API is enabled

### Deployment Failures
1. Check `gcloud app logs tail`
2. Verify all dependencies in requirements.txt
3. Check app.yaml syntax
4. Ensure service account has necessary permissions

## Rolling Back
```bash
# List versions
gcloud app versions list

# Route traffic to previous version
gcloud app versions migrate VERSION_ID
```