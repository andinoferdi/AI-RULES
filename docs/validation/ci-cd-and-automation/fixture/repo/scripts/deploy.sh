#!/usr/bin/env bash
# Usage (AWS keys exported in the shell): ./scripts/deploy.sh <staging|prod> [tag]
set -euo pipefail

ENV="$1"
TAG="${2:-$(git rev-parse --short HEAD)}"
REGISTRY=123456789012.dkr.ecr.eu-west-1.amazonaws.com
IMAGE="$REGISTRY/orders-api:$TAG"

git checkout "$TAG" 2>/dev/null || true
docker build -t "$IMAGE" --build-arg GIT_SHA="$TAG" .
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin "$REGISTRY"
docker push "$IMAGE"

TASKDEF=$(sed "s|__IMAGE__|$IMAGE|; s|__ENV__|$ENV|g" deploy/taskdef.json)
REV=$(aws ecs register-task-definition --cli-input-json "$TASKDEF" \
  --query 'taskDefinition.taskDefinitionArn' --output text)
aws ecs update-service --cluster "orders-$ENV" --service orders-api --task-definition "$REV"

DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id "orders/$ENV/database-url" \
  --query SecretString --output text) npm run db:migrate

echo "Deployed $IMAGE to $ENV"
