"""
==============================================================
API FastAPI - Prédiction des ventes
==============================================================

Charge le modèle entraîné (models/modele_prediction_ventes.pkl) et
les encodeurs (models/encodeurs.pkl), et expose un endpoint /predict
pour obtenir une prédiction de ventes.

Lancement local :
    uvicorn app:app --reload

Documentation interactive une fois lancé :
    http://127.0.0.1:8000/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.model_loader import charger_modele, get_modele, get_encodeurs
from src.predictor import predire_ventes
from src.schemas import DemandePrediction, ReponsePrediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Exécuté une fois au démarrage de l'application
    charger_modele()
    yield
    # (rien à nettoyer à l'arrêt pour l'instant)


app = FastAPI(
    title="API de prédiction des ventes",
    description=(
        "Prédit les ventes journalières d'un magasin pour une famille de "
        "produits donnée, à partir d'un modèle scikit-learn entraîné sur "
        "le dataset Store Sales - Time Series Forecasting."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def accueil():
    return {
        "message": "API de prédiction des ventes - voir /docs pour la documentation",
        "modele_charge": get_modele() is not None,
    }


@app.get("/health")
def sante():
    return {"status": "ok", "modele_charge": get_modele() is not None}


@app.post("/predict", response_model=ReponsePrediction)
def predire(demande: DemandePrediction):
    if get_modele() is None or get_encodeurs() is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Le modèle n'est pas chargé. Vérifiez que les fichiers .pkl "
                "sont présents dans le dossier models/."
            ),
        )
    return ReponsePrediction(ventes_predites=predire_ventes(demande))
