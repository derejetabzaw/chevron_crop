import os 
import cv2
from mmdet.apis import inference_detector, init_detector
from mmcv.image.io import imread
import numpy as np
from aws_save import upload_to_aws
from db_save import db_add_images , add_bin_folder


class Crop_Tapes:
    def __init__(self, git_repo,project_name,mmdetection_dir,config_file,checkpoint_file,directory_path,db_name):
        self.git_repo = git_repo
        self.project_name = project_name
        self.mmdetection_dir = mmdetection_dir
        self.config_file = config_file
        self.checkpoint_file = checkpoint_file
        self.directory_path = directory_path
        self.db_name = db_name
        self.model = init_detector(self.config_file, self.checkpoint_file)


    def add_images_to_db_and_aws(self):
        desired_ext = "jpg"
        convert_ext = [".jpeg" , ".png"] 
        for root, dirs, files in os.walk(self.directory_path):
            print ("Converting Extensions to jpg...")
            for filename in files:
                if filename.endswith(tuple(convert_ext)):
                    image = cv2.imread(os.path.join(root, filename))
                    new_fname = "{}.{}".format(os.path.splitext(filename)[0], desired_ext)
                    small_fname = os.path.join(root, new_fname)
                    cv2.imwrite(small_fname, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                    print ("Removing jpeg, png files...")
                    os.remove(root + '/' + filename)
            for dir in dirs:
                print ("BIN NAME:" , dir)
                bin_id = add_bin_folder(self.db_name,dir)
                print ("BIN ID:" , bin_id)
                print ("----------------")
                for root_1, dirs_1, files_1 in os.walk(str(self.directory_path) + '/' + dir):
                    for image in files_1:
                        img = imread(root_1 + '/' + image)
                        result = inference_detector(self.model, img)
                        inferences = (np.asarray(result)).flatten()
                        W, H, X, Y, U = inferences
                        cropped_image = img[round(H):round(Y), round(W):round(X)]
                        cropped = cv2.imwrite(root_1 + '/' + os.path.basename(image), cropped_image)
                        print("Add images to DB")
                        db_add_images(os.path.basename(image), self.db_name, bin_id)
                        print("Add images to AWS")
                        # upload_to_aws(root_1 + '/' + os.path.basename(image),'nthds-records', '1/tapes/' + str(dir) + '/' + os.path.basename(image))



