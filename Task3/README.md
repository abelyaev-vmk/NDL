# Task3
Language: python3 \
Dependencies:
* Required: openCV, caffe, Easydict

### Face detection
0. `cd lib && make all && cd -`
1. Download [pretrained model](https://drive.google.com/open?id=0Bwbjnpfi3crQRGVwNFF3Ym5HSnM) 
2. Unpack caffemodel and prototxt to models/faces
3. Run ```./exps/face_detection.sh VIDEO.mp4``` \
   This will first create images, parsed from video, then detect faces on all images, and concatenate images with rectangles near faces into result_video.avi


Hint: If you have troubles with hdf5 files when installing caffe, try this out: \
`find . -type f -exec sed -i -e 's^"hdf5.h"^"hdf5/serial/hdf5.h"^g' -e \ 's^"hdf5_hl.h"^"hdf5/serial/hdf5_hl.h"^g' '{}' \;`
