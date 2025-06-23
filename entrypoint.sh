#!/bin/bash
set -e


if [ "$1"="server" ];
then
    echo "Starting server"
    uvicorn main:app --host 0.0.0.0 --port 8491
else
    exec "$@"
fi