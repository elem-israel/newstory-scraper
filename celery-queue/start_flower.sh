#!/bin/bash
flower -A src --port=5555 --broker=$CELERY_BROKER_URL