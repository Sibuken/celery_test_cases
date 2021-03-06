#! /usr/bin/env sh
set -e

DEFAULT_CONCURRENCY=2
DEFAULT_QUEUE=default
DEFAULT_WORKER_NAME=worker
DEFAULT_RABBIT_HOST=rabbit
DEFAULT_RABBIT_PORT=5672

export WORKER_CONCURRENCY=${WORKER_CONCURRENCY:-$DEFAULT_CONCURRENCY}
export WORKER_QUEUE=${WORKER_QUEUE:-$DEFAULT_QUEUE}
export WORKER_NAME=${WORKER_NAME:-$DEFAULT_WORKER_NAME}
export RABBIT_HOST=${RABBIT_HOST:-$DEFAULT_RABBIT_HOST}
export RABBIT_PORT=${RABBIT_PORT:-$DEFAULT_RABBIT_PORT}


while ! nc -z $RABBIT_HOST $RABBIT_PORT; do sleep 3; done
celery -A taskapp worker -E -l INFO --concurrency=$WORKER_CONCURRENCY -n $WORKER_NAME@%h -Q $WORKER_QUEUE