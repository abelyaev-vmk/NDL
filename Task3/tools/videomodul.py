"""
Written by mopkobka

"""

import argparse
import cv2
import json
import os
import os.path as osp
import shutil


def parse():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--path', type=str, default=None)
    argparser.add_argument('-v', '--create-video', action='store_true', default=False)
    argparser.add_argument('-i', '--create-images', action='store_true', default=False)
    argparser.add_argument('-o', '--out', type=str, default=None)
    argparser.add_argument('-m', '--marking', type=str, default=None)
    return argparser.parse_args()


def compute_iou(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter * 1.0 / union


if __name__ == '__main__':
    args = parse()
    assert args.path is not None, 'Need path do video or directory with images'
    if args.create_images:
        assert not osp.isdir(args.path), 'Not a video file "%s"' % args.path
        dir_name = args.out if args.out else ''.join(osp.abspath(args.path).split('.')[:-1]) + '_images'
        if osp.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        video_cap = cv2.VideoCapture(args.path)
        count = 0
        while video_cap.isOpened():
            success, image = video_cap.read()
            if success:
                cv2.imwrite(osp.join(dir_name, 'image%09d.jpg' % count), image)
                count += 1
            else:
                break
        video_cap.release()

    if args.create_video:
        assert osp.isdir(args.path), 'Not a directory "%s"' % args.path
        args.path = osp.abspath(args.path)
        file_name = args.out if args.out else osp.join(osp.dirname(args.path), 'video.avi')
        images = [osp.join(args.path, im_path) for im_path in os.listdir(args.path)]
        images.sort()

        height, width, _ = cv2.imread(images[0]).shape
        video = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'XVID'), 25.0, (width, height))

        if args.marking:
            bboxes = json.load(open(args.marking, 'r'))

        for im_path in images:
            im = cv2.imread(im_path)
            if args.marking:
                rectangles = []
                for bbox in bboxes[im_path.split('/')[-1]]:
                    if bbox['score'] < 0.7:
                        continue
                    x1, x2, y1, y2 = bbox['x'], bbox['x'] + bbox['w'], bbox['y'], bbox['y'] + bbox['h']
                    x1, x2, y1, y2 = list(map(int, (x1, x2, y1, y2)))
                    if not rectangles or all([compute_iou(rect, (x1, y1, x2, y2)) < 0.1 for rect in rectangles]):
                        rectangles.append((x1, y1, x2, y2))
                for x1, y1, x2, y2 in rectangles:
                    cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), thickness=4)
            video.write(im)
        video.release()
