import threading
import os
import numpy as np
import cv2
from PIL import Image
import shutil
from os.path import dirname, join, realpath
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from ultralytics import YOLO
import Models
import Dashboard
import logging

input_dir = "./runs/detect/predict/labels"
output_dir = "preds.json"
image_path = "./Downloader/Data/"

image_width = 1920
image_height = 1080

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Charger le modèle pré-entraîné
model = YOLO('yolov10x.pt')

def load_image(image):
    try:
        img = np.array(Image.open(image).convert('RGB'))
    except Exception as e:
        logging.error(f"Impossible de charger l'image : {image}. Erreur : {e}")
        return None, None
    # mask = np.array(Image.open('mask.png')).convert('RGB') > 0
    img_name = os.path.basename(image).split('-')[-1].split('.')[0]
    return img, img_name

def process_image(file_path):
    logging.info(f"Traitement de l'image : {file_path}")
    if os.path.isfile(file_path):
        img, img_name = load_image(file_path)
        if img is None:
            return
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        logging.info(f"Image chargée : {img_name}")

        prediction = Models.pred(model, img_cv2)
        if isinstance(model, YOLO):
            Models.transform_yolo(input_dir, output_dir, image_width, image_height, img_name)
        else:
            Models.transform_pytorch(prediction, output_dir, img_name)
    else:
        logging.warning(f"Ignoré (n'est pas un fichier) : {file_path}")

class NewImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            logging.info(f"Nouvelle image détectée : {event.src_path}")
            process_image(event.src_path)

def main(image_path):
    if os.path.isfile(output_dir):
        os.remove(output_dir)
    shutil.rmtree(join('./runs'), ignore_errors=True)

    event_handler = NewImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=image_path, recursive=True)
    observer.start()

    logging.info("Surveillance du dossier pour les nouvelles images...")

    def dashboard():
        Dashboard.main()

    dashboard_thread = threading.Thread(target=dashboard)
    dashboard_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    dashboard_thread.join()

if __name__ == "__main__":
    if os.path.isdir(image_path):
        main(image_path)
    else:
        logging.error("Aucun dossier valide.")
