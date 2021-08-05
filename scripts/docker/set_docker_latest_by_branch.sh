#!/bin/bash

BRANCH=$1

case $BRANCH in

  dev | development | desarrollo)
    echo "dev_latest"
    ;;

  staging | "pre" | stage )
    echo "pre_latest"
    ;;

  *)
    echo "latest"
    ;;
esac