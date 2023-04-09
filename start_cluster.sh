#!/bin/sh

IMG_NAME='etl-cluster'
NETWORK_NAME='etl'

docker network create --driver=bridge $NETWORK_NAME
docker run -itd --name $IMG_NAME --net=$NETWORK_NAME --restart=always $IMG_NAME

docker exec -it $IMG_NAME "./bin/run-job.sh"