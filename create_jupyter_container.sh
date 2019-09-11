username="$USER"
user="$(id -u)"

docker run -it -d -p 8888:8888 --name jupyter-environment \
  --user=${user} \
  -e USER=${username} \
  --workdir="$HOME" \
  --volume="$(pwd):$HOME" \
  --volume="/etc/group:/etc/group:ro" \
  --volume="/etc/passwd:/etc/passwd:ro" \
  --volume="/etc/shadow:/etc/shadow:ro" \
  --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
  andreweiner/jupyter-environment:92a151c
