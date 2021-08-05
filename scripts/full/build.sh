source ./scripts/full/ambiente.sh

docker build \
-f $DOCKERFILE_PATH \
--build-arg TAG=$VERSION \
-t $DOCKER_HUB_GROUP/$PROYECTO:$VERSION .
