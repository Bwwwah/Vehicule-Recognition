import os
from os.path import dirname, realpath, join
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import time

coco_filepath = "preds.json"

# Mapping des category_id vers les noms correspondants
category_mapping = {
    0: "Person",
    1: "Bicycle",
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}

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
    try:
        observer.start()
    except OSError as e:
        print(f"Erreur lors du démarrage de l'observer : {e}")
    return observer

def create_charts(coco_data, selected_category, start_date, end_date, min_count):
    annotations = coco_data
    df = pd.DataFrame(annotations)

    if 'time' not in df.columns:
        raise ValueError("Les données JSON doivent inclure un champ 'time'.")

    df['time'] = df['time'].str.replace('_', '')  # Supprimer les underscores
    df['time'] = df['time'].str[:14]  # Prendre seulement les 14 premiers caractères
    df['time'] = pd.to_datetime(df['time'], format='%Y%m%d%H%M%S')

    df['category'] = df['category_id'].map(category_mapping)

    if selected_category:
        df = df[df['category'].isin(selected_category)]
    if start_date:
        df = df[df['time'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['time'] <= pd.to_datetime(end_date)]

    df_counts = df.groupby(['time', 'category']).size().reset_index(name='count')

    if min_count:
        df_counts = df_counts[df_counts['count'] >= min_count]

    fig = px.line(df_counts, x='time', y='count', color='category', title='Distribution des catégories en fonction du temps')
    fig.update_layout(xaxis_title='Temps', yaxis_title='Nombre', margin=dict(l=40, r=20, t=40, b=20))
    return fig

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Filtres", className="card-title"),
                    html.Label("Catégorie"),
                    dcc.Dropdown(
                        id='category-filter',
                        options=[{'label': name, 'value': name} for name in category_mapping.values()],
                        multi=True,
                        className="dcc_control"
                    ),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.Label("Date de début : "),
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        date=None,
                        display_format='YYYY-MM-DD',
                        className="dcc_control"
                    ),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.Label("Date de fin : "),
                    dcc.DatePickerSingle(
                        id='end-date-picker',
                        date=None,
                        display_format='YYYY-MM-DD',
                        className="dcc_control"
                    ),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.Label("Nombre minimum d'éléments : "),
                    dcc.Input(
                        id='min-count-input',
                        type='number',
                        value=0,
                        placeholder="Entrer le nombre minimum",
                        className="dcc_control"
                    ),
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Graphique", className="card-title"),
                    dcc.Graph(id='coco-chart')
                ])
            ])
        ], width=9)
    ]),
    dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0)
])

@app.callback(
    Output('coco-chart', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('category-filter', 'value'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date'),
    Input('min-count-input', 'value')
)
def update_chart(n, selected_category, start_date, end_date, min_count):
    global coco_data
    coco_data = load_coco_data(coco_filepath)
    fig = create_charts(coco_data, selected_category, start_date, end_date, min_count)
    return fig

def main():
    if not os.path.exists(coco_filepath):
        print("Le fichier coco n'est pas la, attente de 1 minute.")
        time.sleep(60)  # Attendre 1 minute

        coco_data = load_coco_data(coco_filepath)
    
        observer = monitor_file(coco_filepath, lambda: print('Fichier COCO mis à jour'))
        app.run_server(host='0.0.0.0', port=8050, debug=False)
        observer.join()
    else:
        coco_data = load_coco_data(coco_filepath)

        observer = monitor_file(coco_filepath, lambda: print('Fichier COCO mis à jour'))
        app.run_server(host='0.0.0.0', port=8050,debug=False)
        observer.join()
    return coco_data

if __name__ == '__main__':

    main()
