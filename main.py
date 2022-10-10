import os 
from os.path import exists, basename, splitext
from clone import clone_from_url
from dotenv import load_dotenv
from mmdet_inference import Crop_Tapes
import argparse
from pathlib import Path
load_dotenv()




parser = argparse.ArgumentParser(description='Crop Tapes')
parser.add_argument('-dir', "--directory", type=Path)
parser.add_argument('-checkpoint', "--checkpoint", type=Path)

args = parser.parse_args()
def dir_path(string):
    if os.path.isdir(string):
        return string 
    else:
        raise NotADirectoryError(string)
def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise NotADirectoryError(string)


directory_path = dir_path(args.directory)


git_repo_url = 'https://github.com/derejetabzaw/mmdetection_object_detection_demo.git'
project_name = os.path.abspath(splitext(basename(git_repo_url))[0])
mmdetection_dir = os.path.join(project_name, "mmdetection")
if not exists(project_name):
    clone_from_url(git_repo_url)
config_file = "configs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712.py"
config_file = config_file.replace("/","\\")
config_fname = os.path.join(project_name, 'mmdetection', config_file)
assert os.path.isfile(config_fname), '`{}` not exist'.format(config_fname)
config_fname = file_path(config_fname)
# checkpoint_file = os.path.join(os.getcwd() + "/epoch_1000_chevron.pth")
checkpoint_file = file_path(args.checkpoint)
assert os.path.isfile(checkpoint_file), '`{}` not exist'.format(checkpoint_file)
# directory_path = os.getcwd() + '/tapes/'
db_name = os.getenv('DB_Name')
project = Crop_Tapes(git_repo_url , project_name , mmdetection_dir , str(config_fname) , str(checkpoint_file),directory_path,db_name)
project.add_images_to_db_and_aws()
