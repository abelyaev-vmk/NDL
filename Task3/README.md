# Task3
Language: python3 \
Dependencies:
* Required: openCV, caffe, Easydict

### Face detection
1. Download [pvanet](https://drive.google.com/open?id=0Bwbjnpfi3crQcXpkdFVSdS12VE0) pretrained model
2. Unpack caffemodel and prototxt to models/faces
3. Run ```./face_detection.sh VIDEO.mp4``` \
   This will first create images, parsed from video, \
   then detect faces on all images, \
   and concatenate images with rectangles near images into result_video.avi