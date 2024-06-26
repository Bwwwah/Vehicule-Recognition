import os
from os import dirname, join
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
from os import path, join, dirname

ROOT_DIR = dirname(dirname(realpath(__file__)))

# Chemin du fichier COCO
coco_filepath = join(ROOT_DIR, 'Deploy', 'preds.json')

class CocoFileHandler(FileSystemEventHandler):
    def __init__(self, filepath, update_callback):
        self.filepath = filepath
        self.update_callback = update_callback

    def on_modified(self, event):
        if event.src_path == self.filepath:
            self.update_callback()

def load_coco_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def monitor_file(filepath, update_callback):
    event_handler = CocoFileHandler(filepath, update_callback)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(filepath), recursive=False)
    observer.start()
    return observer

def create_charts(coco_data):
    # Exemple de transformation des données COCO en DataFrame pour un graphique
    annotations = coco_data['annotations']
    df = pd.DataFrame(annotations)
    
    # Création d'un graphique simple (par exemple, histogramme des catégories)
    fig = px.histogram(df, x='category_id', title='Distribution des catégories')
    return fig

# Initialisation de l'application Dash
app = Dash(__name__)

# Chargement initial des données COCO
coco_data = load_coco_data(coco_filepath)

# Layout de l'application Dash
app.layout = html.Div([
    dcc.Graph(id='coco-chart'),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)  # Mise à jour toutes les minutes
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output('coco-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_chart(n):
    global coco_data
    coco_data = load_coco_data(coco_filepath)
    fig = create_charts(coco_data)
    return fig

if __name__ == '__main__':
    # Surveillance du fichier COCO
    observer = monitor_file(coco_filepath, lambda: print('Fichier COCO mis à jour'))
    app.run_server(debug=True)
    observer.stop()
    observer.join()
