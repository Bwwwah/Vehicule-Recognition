import os
import json
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import torch, torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn, retinanet_resnet50_fpn
from torchvision.transforms import functional as F

from os.path import dirname, realpath, join

def transform_pytorch(predictions, output_file, img_name, results_dir, allowed_category_ids=[0, 1, 2, 3, 4, 5, 6, 7]):
    # Charger les détections existantes depuis le fichier de sortie s'il existe
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_detections = json.load(file)
    else:
        existing_detections = []

    if os.path.exists(results_dir):
        with open(results_dir, 'r') as file:
            results = json.load(file)
            images = results['images']
            image_id = None
            for image in images:
                if img_name in image['file_name']:
                    image_id = image['id']
                    break
            if image_id is None:
                raise ValueError(f"Image name {img_name} not found in results")
    else:
        raise FileNotFoundError(f"Results file {results_dir} not found")

    category_map = {
        0: 5,
        1: 0,
        2: 2,
        3: 4,
        5: 1,
        7: 7
    }

    for prediction in predictions:
        detections = []

        # Convertir les tensors en listes
        boxes = prediction['boxes'].tolist()
        labels = prediction['labels'].tolist()
        scores = prediction['scores'].tolist()

        for i in range(len(boxes)):
            box = boxes[i]
            label = labels[i]
            score = scores[i]

            # Ajouter la condition pour filtrer par les category_id autorisés
            if label in category_map:
                x_min, y_min, x_max, y_max = box
                width = x_max - x_min
                height = y_max - y_min
                bbox = [x_min, y_min, width, height]

                detection = {
                    "image_id": image_id,
                    "category_id": category_map[label],  # Convertir le category_id
                    "bbox": bbox,
                    "score": score,
                    "time": img_name 
                }
                detections.append(detection)

        existing_detections.extend(detections)

    with open(output_file, 'w') as out_file:
        json.dump(existing_detections, out_file, indent=4)

def transform_yolo(input_dir, output_file, image_width, image_height, img_name):
    files = os.listdir(input_dir)
    input_file = os.path.join(input_dir, files[0])

    # Charger les détections existantes depuis le fichier de sortie s'il existe
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_detections = json.load(file)
    else:
        existing_detections = []  

    max_image_id = max([detection['image_id'] for detection in existing_detections], default=0)
    new_image_id = max_image_id + 1

    detections = []

    # Dictionnaire de mappage des category_id
    category_map = {
        0: 5,
        1: 0,
        2: 2,
        3: 4,
        5: 1,
        7: 7
    }

    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            category_id = int(parts[0])

            # Vérifier si category_id est dans la liste autorisée
            if category_id in category_map:
                # Remplacer category_id par sa nouvelle valeur
                new_category_id = category_map[category_id]

                x_center = float(parts[1]) * image_width
                y_center = float(parts[2]) * image_height
                width = float(parts[3]) * image_width
                height = float(parts[4]) * image_height
                score = float(parts[5])

                # Convertir les coordonnées du centre au format COCO [x_min, y_min, width, height]
                x_min = x_center - (width / 2)
                y_min = y_center - (height / 2)

                bbox = [x_min, y_min, width, height]

                detection = {
                    "image_id": new_image_id,
                    "category_id": new_category_id,
                    "bbox": bbox,
                    "score": score,
                    "time": img_name
                }
                detections.append(detection)


    with open(input_file, 'w') as fichier:
            pass
    existing_detections.extend(detections)

    with open(output_file, 'w') as out_file:
        json.dump(existing_detections, out_file, indent=4)

def pred(model, img_cv2):
    img_tensor = F.to_tensor(img_cv2)
    if isinstance(model, YOLO):
        model.predict(img_cv2, save_conf=True, save_txt=True, conf=0.3)
    elif (model, fasterrcnn_resnet50_fpn(pretrained=True)):
        model.eval()
        with torch.no_grad():
            prediction = model([img_tensor])
            return prediction
    # if isinstance(model, torchvision.models.detection.retinanet_resnet50_fpn):
    #     model.eval()
    #     #TODO
    #     with torch.no_grad():
    #         prediction = model([img_cv2])
    #         print(prediction)
    else:
        print("Modèle non pris en charge.")