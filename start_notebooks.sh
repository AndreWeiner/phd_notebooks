CONTAINER_NAME="jupyter-environment"
docker start $CONTAINER_NAME
docker exec -it $CONTAINER_NAME /bin/bash notebooks/start.sh
