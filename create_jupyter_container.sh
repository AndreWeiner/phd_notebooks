DATA_LOCAL="${PWD}/data/"
NOTEBOOKS_LOCAL="${PWD}/notebooks/"
OUTPUT_LOCAL="${PWD}/output/"
DATA_CONTAINER="/home/jupyter_user/data/"
NOTEBOOKS_CONTAINER="/home/jupyter_user/notebooks/"
OUTPUT_CONTAINER="/home/jupyter_user/output/"

docker run -it -d -p 8888:8888 --name jupyter-environment \
  --volume="$DATA_LOCAL:$DATA_CONTAINER" \
  --volume="$NOTEBOOKS_LOCAL:$NOTEBOOKS_CONTAINER" \
  --volume="$OUTPUT_LOCAL:$OUTPUT_CONTAINER" \
  andreweiner/jupyter-environment:v1
