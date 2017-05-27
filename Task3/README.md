# Task2
Language: python3 \
Dependencies:
* Required: openCV, caffe, Easydict

### Face detection
1. Download and unpack [pvanet](https://drive.google.com/open?id=0Bwbjnpfi3crQcXpkdFVSdS12VE0) pretrained model
2. Run ```./tools/parse_video.py PATH_TO_VIDEO PATH_TO_MARKING```
3. Configure exps/faces with your pathes (you can add several datasets to test)
4. Run ```./tools/test_net.py --gpu 0 --net PATH_TO_CAFFEMODEL --cfg exps/faces/config.yaml --exp_dir faces```
5. Run ```./tools/make_video.py PATH_TO_IMAGES PATH_TO_MARKING```