#!/bin/bash
export CELERY_BROKER_URL=redis://redis:$REDIS_PASSWORD@$REDIS_HOST:$REDIS_PORT/0
export CELERY_RESULT_BACKEND=redis://redis:$REDIS_PASSWORD@$REDIS_HOST:$REDIS_PORT/0
celery -A src worker --loglevel=info -Q $QUEUES --concurrency 1