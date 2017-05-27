# Task2
Language: python3 \
Dependencies:
* Required: openCV, caffe, Easydict

### Face detection
1. Compile caffe, see manual [here](http://caffe.berkeleyvision.org/installation.html) \
   If you are using Docker, check [my docker git](https://github.com/abelyaev-vmk/admin/tree/master/dockerfiles) to full cuda+openCV+caffe on docker installation pipeline
2. Download and unpack [pvanet](https://drive.google.com/open?id=0Bwbjnpfi3crQcXpkdFVSdS12VE0) pretrained model
3. Run ```./tools/parse_video.py PATH_TO_VIDEO PATH_TO_MARKING```
4. Configure exps/faces with your pathes (you can add several datasets to test)
5. Run ```./tools/test_net.py --gpu 0 --net PATH_TO_CAFFEMODEL --cfg exps/faces/config.yaml --exp_dir faces```
6. Run ```./tools/make_video.py PATH_TO_IMAGES PATH_TO_MARKING```
