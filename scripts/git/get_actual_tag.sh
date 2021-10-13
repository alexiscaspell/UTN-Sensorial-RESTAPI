# LATEST_TAG=$(git describe --tags `git rev-list --tags --max-count=1`)
# LATEST_TAG="${LATEST_TAG/'refs/heads/'/''}"
# LATEST_TAG="${LATEST_TAG/'v'/''}"
LATEST_TAG=$(git tag |sort -rV | head -1)

echo $LATEST_TAG

