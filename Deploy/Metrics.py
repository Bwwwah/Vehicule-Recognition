import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from os.path import dirname, realpath, join

ROOT_DIR = dirname(dirname(realpath(__file__)))

def main():
    # Chemins vers les fichiers JSON ground truth et prédictions au format COCO
    annotations_gt_file = join(ROOT_DIR, 'Dataset', 'result.json')
    predictions_file = join(ROOT_DIR, 'Deploy', 'preds.json')

    # Chargement des données ground truth
    coco_gt = COCO(annotations_gt_file)
    
    with open(predictions_file, 'r') as f:
        predictions = json.load(f)

    # Convertir les prédictions en format COCO
    coco_dt = coco_gt.loadRes(predictions)

    # Initialiser l'évaluateur COCO
    coco_eval = COCOeval(coco_gt, coco_dt, 'bbox')

    # Calculer les statistiques
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()

if __name__ == "__main__":
    main()

