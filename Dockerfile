# use Ubuntu 18.04 (bionic) as base
FROM ubuntu:bionic
LABEL maintainer="Andre Weiner <weiner@mma.tu-darmstadt.de>"

# argument to avoid user interaction during installation
ARG DEBIAN_FRONTEND=noninteractive

# install pip (python 3)
RUN apt-get update && apt-get install -y  \
  python3-matplotlib \
  python3-numpy \
  python3-pandas \
  python3-pip \
  python3-scipy \
  python3-tqdm && \
  rm -rf /var/lib/apt/lists/*

# update pip and install scikit learn and pytorch
RUN pip3 install \
  jupyter \
  scikit-learn \
  torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# expose port to run in browser
EXPOSE 8888
