#!/bin/bash
# Deployment script for ClimateAPI
# Usage: ./deploy.sh [staging|production]

set -e  # Exit on error

ENVIRONMENT=${1:-staging}
PROJECT_NAME="climate-prediction"

if [ "$ENVIRONMENT" = "production" ]; then
  APP_NAME="climate-api"
  REPLICAS=3
else
  APP_NAME="climate-api-staging"
  REPLICAS=1
fi

echo "========================================="
echo "Deploying Climate API"
echo "========================================="
echo "Environment: $ENVIRONMENT"
echo "App Name: $APP_NAME"
echo "Project: $PROJECT_NAME"
echo "Replicas: $REPLICAS"
echo "========================================="

outerbounds app deploy \
  --name "$APP_NAME" \
  --project "$PROJECT_NAME" \
  --python 3.10 \
  --package-src-path deployments/climate-api \
  --command "python app.py" \
  --requirements requirements.txt \
  --cpu 2 \
  --memory 8192 \
  --replicas "$REPLICAS" \
  --min-replicas 1 \
  --max-replicas 3 \
  --scaling-metric avg_rpm=100 \
  --public --port 8000

echo ""
echo "========================================="
echo "Deployment complete!"
echo "========================================="
echo "Check status with:"
echo "  outerbounds app list --project $PROJECT_NAME"
echo ""
