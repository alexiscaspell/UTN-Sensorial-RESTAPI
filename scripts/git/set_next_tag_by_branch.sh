#!/bin/bash

LATEST_TAG=$1
BRANCH=$2

IFS='.' read -ra ADDR <<< "$LATEST_TAG"
for i in "${ADDR[@]}"; do
  subtags+=($i)
done

v_part1=${subtags[0]}
v_part2=${subtags[1]}
v_part3=${subtags[2]}

case $BRANCH in

  dev | development | desarrollo | desa )
    v_part3=$(($v_part3+1))
    ;;

  staging | "pre" | stage | qa )
    v_part3=0
    v_part2=$(($v_part2+1))
    ;;

  *)
    v_part3=0
    v_part2=0
    v_part1=$(($v_part1+1))
    ;;
esac

NEXT_TAG="$v_part1.$v_part2.$v_part3"

echo $NEXT_TAG

