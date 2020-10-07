#!/bin/bash
flower -A src --port=5555 --broker="redis://redis:$REDIS_PASSWORD@REDIS_HOST"