import os 
import sys
import cv2
from mmdet.models.detectors import BaseDetector
from mmdet.apis import inference_detector, init_detector
from mmcv.image.io import imread
import numpy as np
from os.path import exists, basename, splitext
from clone import clone_from_url
from aws_save import upload_to_aws
from db_save import db_add_images , bin_id_select , add_bin_folder
images = []
image_paths = []
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv('DB_Name')



git_repo_url = 'https://github.com/derejetabzaw/mmdetection_object_detection_demo.git'

project_name = os.path.abspath(splitext(basename(git_repo_url))[0])

if not exists(project_name):
    clone_from_url(git_repo_url)
config_file = "configs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712.py"
config_fname = os.path.join(project_name, 'mmdetection', config_file)
print (config_fname)
assert os.path.isfile(config_fname), '`{}` not exist'.format(config_fname)
image_dirs = os.getcwd() + '/tapes/'



mmdetection_dir = os.path.join(project_name, "mmdetection")


checkpoint_file = os.path.join(os.getcwd() + "/epoch_1000_chevron.pth")
assert os.path.isfile(checkpoint_file), '`{}` not exist'.format(checkpoint_file)
model = init_detector(config_fname, checkpoint_file)

directory_path = os.getcwd() + '/tapes'
desired_ext = "jpg"
convert_ext = [".jpeg" , ".png"] 
for root, dirs, files in os.walk(directory_path):
    dirname = root.split(os.path.sep)[-1]
    print ("Converting Extensions to jpg...")

    for filename in files:
        if filename.endswith(tuple(convert_ext)):
            image = cv2.imread(os.path.join(root, filename))
            new_fname = "{}.{}".format(os.path.splitext(filename)[0], desired_ext)
            small_fname = os.path.join(root, new_fname)
            cv2.imwrite(small_fname, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            print ("Removing jpeg, png files...")
            os.remove(root + '/' + filename)




bin_names = []
bin_ids = []
for root, dirs, files in os.walk(directory_path):
    for dir in dirs:
        print ("BIN_NAME:" , dir)
        bin_id = add_bin_folder(db_name,dir)
        print ("BIN_ID" , bin_id)
        print ("----------------")
        for root_1, dirs_1, files_1 in os.walk(directory_path + '/' + dir):
            for image in files_1:
                img = imread(root_1 + '/' + image)
                result = inference_detector(model, img)
                inferences = (np.asarray(result)).flatten()
                W, H, X, Y, U = inferences
                cropped_image = img[round(H):round(Y), round(W):round(X)]
                cropped = cv2.imwrite(root_1 + '/' + os.path.basename(image), cropped_image)
                image_paths.append(os.path.basename(image))
                print("Add images to DB")
                
                db_add_images(os.path.basename(image), db_name,dir, bin_id)
                print("Add images to AWS")
                upload_to_aws(root_1 + '/' + os.path.basename(image),'nthds-records', '1/tapes/' + str(dir) + '/' + os.path.basename(image))




