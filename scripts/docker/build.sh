#!/bin/sh
#!/bin/sh

. scripts/docker/ambiente.sh "$1"

echo $DOCKER_HUB_GROUP/$PROYECTO:$VERSION

docker build \
-f $DOCKERFILE_PATH \
--build-arg TAG=$VERSION \
-t $DOCKER_HUB_GROUP/$PROYECTO:$VERSION .
