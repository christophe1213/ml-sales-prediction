"""
Tests de l'API de prédiction des ventes (app.py).
Lancement : pytest tests/ -v
"""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_accueil():
    """Vérifie que la racine répond correctement."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Vérifie l'endpoint de santé."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_structure_valide():
    """Vérifie que /predict répond (200) ou refuse proprement (400/503)
    selon que le modèle est chargé et la valeur catégorielle connue,
    mais ne plante jamais avec une erreur 500 (erreur serveur non gérée)."""
    payload = {
        "store_nbr": 1,
        "family": "GROCERY I",
        "onpromotion": 5,
        "city": "Quito",
        "state": "Pichincha",
        "type": "D",
        "cluster": 13,
        "dcoilwtico": 65.5,
        "est_ferie": 0,
        "date": "2017-08-15",
        "ventes_lag_7": 1200.0,
        "ventes_lag_14": 1150.0,
        "ventes_lag_30": 1100.0,
        "ventes_mm_7": 1180.0,
        "ventes_mm_30": 1120.0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code in (200, 400, 503)


def test_predict_champ_manquant():
    """Une requête incomplète doit être rejetée avec une erreur de validation (422)."""
    response = client.post("/predict", json={"store_nbr": 1})
    assert response.status_code == 422
