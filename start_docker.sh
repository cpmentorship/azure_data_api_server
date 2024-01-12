#!/bin/sh

docker run -it --rm \
    --user $(id -u):$(id -g) \
    --group-add users \
    -v "$(pwd)":/app \
    -p 5001:5000 \
    azure_data_api_server:1.0