# Task3
Language: python3 \
Dependencies:
* Required: openCV, caffe, Easydict

### Face detection
1. Download [pretrained model](https://drive.google.com/open?id=0Bwbjnpfi3crQRGVwNFF3Ym5HSnM) 
2. Unpack caffemodel and prototxt to models/faces
3. Run ```./exps/face_detection.sh VIDEO.mp4``` \
   This will first create images, parsed from video, then detect faces on all images, and concatenate images with rectangles near images into result_video.avi
