LATEST_TAG=$(git describe --tags `git rev-list --tags --max-count=1`)
LATEST_TAG="${LATEST_TAG/'refs/heads/'/''}"
LATEST_TAG="${LATEST_TAG/'v'/''}"

echo $LATEST_TAG

