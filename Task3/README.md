# Task3
Language: python3 \
Dependencies:
* Required: openCV, caffe, Easydict

### Face detection
<<<<<<< HEAD
1. Download [pvanet](https://drive.google.com/open?id=0Bwbjnpfi3crQcXpkdFVSdS12VE0) pretrained model
2. Unpack caffemodel and prototxt to models/faces
3. Run ```./face_detection.sh VIDEO.mp4``` \
   This will first create images, parsed from video, \
   then detect faces on all images, \
   and concatenate images with rectangles near images into result_video.avi
=======
1. Compile caffe, see manual [here](http://caffe.berkeleyvision.org/installation.html) \
   If you are using Docker, check [my docker git](https://github.com/abelyaev-vmk/admin/tree/master/dockerfiles) to full cuda+openCV+caffe on docker installation pipeline
2. Download and unpack [pvanet](https://drive.google.com/open?id=0Bwbjnpfi3crQcXpkdFVSdS12VE0) pretrained model
3. Run ```./tools/parse_video.py PATH_TO_VIDEO PATH_TO_MARKING```
4. Configure exps/faces with your pathes (you can add several datasets to test)
5. Run ```./tools/test_net.py --gpu 0 --net PATH_TO_CAFFEMODEL --cfg exps/faces/config.yaml --exp_dir faces```
6. Run ```./tools/make_video.py PATH_TO_IMAGES PATH_TO_MARKING```
>>>>>>> 337a747551cc38fa2c332a463631bf9c3c3b944a
