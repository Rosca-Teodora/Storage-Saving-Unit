# older, stable version of Ubuntu as base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y gcc gcc-multilib make && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
CMD ["bash"]