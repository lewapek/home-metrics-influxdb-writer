#!/bin/sh

ARCHITECTURE=`lscpu | grep Architecture | awk '{print $2}'`
echo "Found architecture: ${ARCHITECTURE}"

VERSION=`cat version`

case "${ARCHITECTURE}" in
    "x86_64" )
        echo "Architecture matches 'x86_64'"
        ;;
    "armv6l" )
        echo "Architecture matches 'armv6l'"
        VERSION="${VERSION}-armv6l"
        ;;
    "armv7l" )
        echo "Architecture matches 'armv7l'"
        VERSION="${VERSION}-armv7l"
        ;;
    "asd"    )
        echo "Could not match any architecture"
        exit 1
        ;;
esac

echo "Building version ${VERSION}"

docker build -t lewap/http-to-influx-writer:${VERSION} .
