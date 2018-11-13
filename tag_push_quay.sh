docker pull namsyvo/gdc_tosvc_tools:$1
docker tag namsyvo/gdc_tosvc_tools:$1 quay.io/ncigdc/gdc_tosvc_tools:$1
docker push quay.io/ncigdc/gdc_tosvc_tools:$1
