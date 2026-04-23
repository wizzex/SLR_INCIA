import subprocess
import webbrowser
import time
import os
import json
import networkx as nx
from test_cytoscape import load_model, export_to_cytoscape  # adapte le chemin

def launch_visualizer(json_path):
    # Se placer dans le bon dossier EN PREMIER
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Générer le graph.json (sera créé dans src/)
    G = load_model(json_path)
    export_to_cytoscape(G)
    print("✔ graph.json generated")

    # Lancer le serveur HTTP
    server = subprocess.Popen(["python", "-m", "http.server", "8000"])
    time.sleep(1)

    webbrowser.open("http://localhost:8000/visualize.html")
    
    return server

