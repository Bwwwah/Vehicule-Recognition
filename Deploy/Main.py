import os
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from ultralytics import YOLO
import shutil
import Models
from os.path import dirname, join, realpath
import torchvision.models.detection as tc

ROOT_DIR = dirname(dirname(realpath(__file__)))
DEPLOY_DIR = join(ROOT_DIR, 'Deploy')

input_dir = join(ROOT_DIR, 'runs', 'detect', 'predict', 'labels')
output_dir = join(DEPLOY_DIR, 'preds.json')
results_dir = join(ROOT_DIR, 'Dataset', 'result.json')

image_width = 1920
image_height = 1080

# Charger le modèle pré-entraîné
# model = tc.fasterrcnn_resnet50_fpn(pretrained=True)
model = tc.retinanet_resnet50_fpn(pretrained=True)
# model = YOLO('yolov10x.pt')

def load_image(image):
    try:
        img = np.array(Image.open(image).convert('RGB'))
    except:
        print(f"Impossible de charger l'image : {image}")
        return None, None
    mask = np.array(Image.open("./Deploy/mask.png").convert('RGB')) > 0
    img = img * mask
    img_name = image.split('-')[-1]
    img_name = img_name.split('.')[0]

    return img, img_name

def main(folder_path):
    if os.path.isfile(join(DEPLOY_DIR, 'preds.json')):
        os.remove(join(DEPLOY_DIR, 'preds.json'))
    shutil.rmtree(join(ROOT_DIR, 'runs'), ignore_errors=True)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            img, img_name = load_image(file_path)
            if img is None:
                continue
            img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            print(f"Image chargée : {img_name}")

            prediction = Models.pred(model, img_cv2)
            if isinstance (model, YOLO):
                Models.transform_yolo(input_dir, output_dir, image_width, image_height, img_name, results_dir)
            else :
                Models.transform_pytorch(prediction, output_dir, img_name, results_dir)
        else:
            print(f"Ignoré (n'est pas un fichier) : {file_name}")
    shutil.rmtree(join(ROOT_DIR, 'runs'), ignore_errors=True)


if __name__ == "__main__":
    folder_path = join(ROOT_DIR, 'Dataset', 'Images')
    
    if folder_path:
        main(folder_path)
    else:
        print("Aucun dossier.")
