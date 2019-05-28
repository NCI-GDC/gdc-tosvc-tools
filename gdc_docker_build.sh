#!/bin/bash
# Uses the commit from git repo to build and tag the image

docker_build () {
    command docker build \
        --build-arg http_proxy=$http_proxy \
        --build-arg https_proxy=$https_proxy \
        --build-arg no_proxy=$no_proxy \
        "$@"
}

quay="quay.io/ncigdc/gdc_tosvc_tools"
version=$(git log --first-parent --max-count=1 --format=format:%H)
imagetag="${quay}:${version}"

echo "Building tag: $imagetag"
docker_build -t $imagetag .
