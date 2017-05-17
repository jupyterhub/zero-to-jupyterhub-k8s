FROM jupyterhub/configurable-http-proxy:2.0.1

CMD configurable-http-proxy --ip 0.0.0.0 --port 8000 \
    --api-ip 0.0.0.0 --api-port 8001 \
    --default-target http://${HUB_SERVICE_HOST}:${HUB_SERVICE_PORT} \
    --error-target http://${HUB_SERVICE_HOST}:${HUB_SERVICE_PORT}
