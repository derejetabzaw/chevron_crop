import os 
import sys
import cv2
from mmdet.models.detectors import BaseDetector
from mmdet.apis import inference_detector, init_detector
from mmcv.image.io import imread
import numpy as np
from os.path import exists, basename, splitext
from clone import clone_from_url
images = []


git_repo_url = 'https://github.com/derejetabzaw/mmdetection_object_detection_demo.git'

project_name = os.path.abspath(splitext(basename(git_repo_url))[0])

if not exists(project_name):
    clone_from_url(git_repo_url)
config_file = "configs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712.py"
config_fname = os.path.join(project_name, 'mmdetection', config_file)
print (config_fname)
assert os.path.isfile(config_fname), '`{}` not exist'.format(config_fname)
image_dirs = project_name + "/data/VOC2007/JPEGImages/" 



mmdetection_dir = os.path.join(project_name, "mmdetection")


checkpoint_file = os.path.join(os.getcwd() + "/epoch_1000_chevron.pth")
assert os.path.isfile(checkpoint_file), '`{}` not exist'.format(checkpoint_file)




model = init_detector(config_fname, checkpoint_file)
if not os.path.exists("cropped"):
    os.makedirs("cropped")
cropped_dirs = os.getcwd() + "/cropped/"

def image_files_list(path):
    files = os.listdir(path)
    for file in files:
        if file.lower().endswith('.jpg'):
            images.append(path + file)
    return images
 
    
image_files = image_files_list(image_dirs)

for idx , image in enumerate(image_files):
    img = imread(image)
    result = inference_detector(model, img)
    inferences = (np.asarray(result)).flatten()
    W, H, X, Y, U = inferences
    cropped_image = img[round(H):round(Y), round(W):round(X)]
    cropped = cv2.imwrite(cropped_dirs + os.path.basename(image), cropped_image)





