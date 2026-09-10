"""
Construction du vecteur de features à partir d'une requête, et
appel du modèle pour obtenir une prédiction.
"""
import pandas as pd

from src.config import FEATURES
from src.model_loader import get_modele, encoder_categorie
from src.schemas import DemandePrediction


def construire_ligne_features(demande: DemandePrediction) -> pd.DataFrame:
    """Transforme une requête validée en une ligne de features, dans
    l'ordre exact attendu par le modèle."""
    date = pd.to_datetime(demande.date)

    ligne = {
        "store_nbr": demande.store_nbr,
        "family": encoder_categorie("family", demande.family),
        "onpromotion": demande.onpromotion,
        "city": encoder_categorie("city", demande.city),
        "state": encoder_categorie("state", demande.state),
        "type": encoder_categorie("type", demande.type),
        "cluster": demande.cluster,
        "dcoilwtico": demande.dcoilwtico,
        "EstFerie": demande.est_ferie,
        "Annee": date.year,
        "Mois": date.month,
        "Jour": date.day,
        "JourSemaine": date.dayofweek,
        "Semaine": int(date.isocalendar().week),
        "FinDeMois": 1 if date.day >= 25 else 0,
        "Ventes_Lag_7": demande.ventes_lag_7,
        "Ventes_Lag_14": demande.ventes_lag_14,
        "Ventes_Lag_30": demande.ventes_lag_30,
        "Ventes_MM_7": demande.ventes_mm_7,
        "Ventes_MM_30": demande.ventes_mm_30,
    }
    return pd.DataFrame([ligne])[FEATURES]


def predire_ventes(demande: DemandePrediction) -> float:
    """Construit les features, appelle le modèle, et retourne une
    prédiction de ventes toujours positive ou nulle."""
    X = construire_ligne_features(demande)
    prediction = get_modele().predict(X)[0]
    return round(max(0.0, float(prediction)), 2)
