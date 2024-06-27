import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from os.path import dirname, realpath, join
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

ROOT_DIR = dirname(dirname(realpath(__file__)))

def calculate_f1_score(precision, recall):
    return 2 * (precision * recall) / (precision + recall + 1e-12)  # Adding a small epsilon to avoid division by zero

def create_confusion_matrix(coco_gt, coco_dt):
    gt_labels = []
    dt_labels = []
    
    img_ids = coco_gt.getImgIds()
    for img_id in img_ids:
        # Obtenir les annotations ground truth
        ann_ids = coco_gt.getAnnIds(imgIds=img_id)
        anns = coco_gt.loadAnns(ann_ids)
        img_gt_labels = [ann['category_id'] for ann in anns]

        # Obtenir les prédictions
        dt_ids = coco_dt.getAnnIds(imgIds=img_id)
        dts = coco_dt.loadAnns(dt_ids)
        img_dt_labels = [dt['category_id'] for dt in dts]

        # Alignement des étiquettes ground truth et prédictions par image
        for gt_label in img_gt_labels:
            gt_labels.append(gt_label)
            if img_dt_labels:
                dt_labels.append(img_dt_labels.pop(0))
            else:
                dt_labels.append(-1)  # Etiquette neutre pour les correspondances manquantes

        # Pour les prédictions restantes sans annotations correspondantes
        while img_dt_labels:
            gt_labels.append(-1)  # Etiquette neutre pour les correspondances manquantes
            dt_labels.append(img_dt_labels.pop(0))

    # Calculer la matrice de confusion
    labels = sorted(set(gt_labels + dt_labels))
    conf_matrix = confusion_matrix(gt_labels, dt_labels, labels=labels)
    
    return conf_matrix, labels

def plot_and_save_confusion_matrix(conf_matrix, labels, output_path):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Blues', ax=ax)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.savefig(output_path)
    plt.close()

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

    # Retrieve average precision and recall
    avg_precision = coco_eval.stats[0]  # average precision
    avg_recall = coco_eval.stats[1]     # average recall

    # Calculate F1 score
    f1_score = calculate_f1_score(avg_precision, avg_recall)

    print(f"F1 score global: {f1_score}")

    # Créer et sauvegarder la matrice de confusion
    conf_matrix, labels = create_confusion_matrix(coco_gt, coco_dt)
    output_path = join(ROOT_DIR, 'confusion_matrix.png')
    plot_and_save_confusion_matrix(conf_matrix, labels, output_path)
    print(f"Confusion matrix saved to {output_path}")

if __name__ == "__main__":
    main()
