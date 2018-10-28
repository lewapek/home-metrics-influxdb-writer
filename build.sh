#!/bin/sh

ARCHITECTURE=`lscpu | grep Architecture | awk '{print $2}'`
echo "Found architecture: ${ARCHITECTURE}"

VERSION=`cat version`

case "${ARCHITECTURE}" in
    "x86_64" )
        echo "Architecture matches 'x86_64'"
        ;;
    "armv6"  )
        echo "Architecture matches 'armv6'"
        VERSION="${VERSION}-arm6"
        ;;
    "armv7"  )
        echo "Architecture matches 'armv7'"
        VERSION="${VERSION}-arm7"
        ''
esac

echo "Building version ${VERSION}"

docker build -t lewap/http-to-influx-writer:${VERSION} .
