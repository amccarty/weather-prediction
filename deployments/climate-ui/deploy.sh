#!/bin/bash
# Deployment script for Climate UI Dashboard
# Usage: ./deploy.sh [staging|production]

set -e  # Exit on error

ENVIRONMENT=${1:-staging}
PROJECT_NAME="climate-prediction"

if [ "$ENVIRONMENT" = "production" ]; then
  APP_NAME="climate-ui"
  REPLICAS=2
else
  APP_NAME="climate-ui-staging"
  REPLICAS=1
fi

echo "========================================="
echo "Deploying Climate UI Dashboard"
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
  --package-src-path deployments/climate-ui \
  --command "python app.py" \
  --requirements requirements.txt \
  --cpu 1 \
  --memory 2048 \
  --replicas "$REPLICAS" \
  --min-replicas 1 \
  --max-replicas "$REPLICAS" \
  --public --port 8001

echo ""
echo "========================================="
echo "Deployment complete!"
echo "========================================="
echo "Check status with:"
echo "  outerbounds app list --project $PROJECT_NAME"
echo ""
