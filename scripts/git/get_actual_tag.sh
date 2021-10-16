LATEST_TAG=$(git tag |sort -rV | head -1)
LATEST_TAG="${LATEST_TAG/'refs/heads/'/''}"
LATEST_TAG="${LATEST_TAG/'v'/''}"

echo $LATEST_TAG

