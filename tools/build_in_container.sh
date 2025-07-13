#!/bin/sh

cd "$(dirname "$0")"

docker build -t tuxedo-drivers-builder . -f Dockerfile.build

docker run -it -v "$PWD":/build tuxedo-drivers-builder /build/tools/build.sh "$@"
