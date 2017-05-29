#!/usr/bin/env bash

VIDEO_NAME=$1
IMAGES_DIR='data/images_from_video'
LOGS='exps/faces/logs.txt'

echo "Creating images"
python3 ./tools/videomodul.py --create-images --path=${VIDEO_NAME} --out=${IMAGES_DIR}
echo "Start CNN"
python3 ./tools/test_net.py --gpu 0 \
    --net models/faces/faces.caffemodel \
    --proto models/faces/faces.prototxt \
    --cfg exps/faces/config.yml \
    --exp_dir faces > ${LOGS}
VIDEOSET=`cat ${LOGS} | grep "Output detections file: " | cut -f4- -d" "`
echo "Creating video"
python3 ./tools/videomodul.py --create-video --path=${IMAGES_DIR} --marking=${VIDEOSET} --out=result_video.avi
