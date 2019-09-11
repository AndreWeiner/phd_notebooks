CONTAINER_NAME="jupyter-environment"
docker start $CONTAINER_NAME
docker exec -it $CONTAINER_NAME /bin/bash start_notebook.sh
