#!/bin/bash

for SRC in *.png; do
    OUT=${SRC/.png/.ico}
    if [ ! -e ${OUT} ]; then
        convert ${SRC} -define icon:auto-resize=256,128,64,48,32,16 ${OUT}
    fi
done
