from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from typing import List
import time
from monitoring import ModelMonitor

app = FastAPI()

# Chargement du modèle
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    model = None

# Création du moniteur
monitor = ModelMonitor()

class WineFeatures(BaseModel):
    features: List[float]

@app.get("/")
def home():
    return {"message": "Wine Quality Prediction API"}

@app.post("/predict")
async def predict(features: WineFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convertir les features en DataFrame
        df = pd.DataFrame([features.features], columns=[
            'alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', 'magnesium',
            'total_phenols', 'flavanoids', 'nonflavanoid_phenols', 'proanthocyanins',
            'color_intensity', 'hue', 'od280/od315_of_diluted_wines', 'proline'
        ])
        
        start_time = time.time()
        prediction = model.predict(df)[0]
        latency = time.time() - start_time
        
        # Log la prédiction pour le monitoring
        monitor.log_prediction(df, prediction, latency)
        
        return {"prediction": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_reports")
async def generate_reports():
    try:
        monitor.generate_data_drift_report()
        monitor.generate_data_stability_test()
        return {"message": "Reports generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Métriques Prometheus
Instrumentator().instrument(app).expose(app)
