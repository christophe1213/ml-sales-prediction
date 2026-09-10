"""
Chargement du modèle entraîné et des encodeurs catégoriels.

Le chargement se fait une seule fois au démarrage de l'API (voir le
lifespan défini dans app.py), puis les objets sont réutilisés pour
chaque requête via get_modele() / get_encodeurs().
"""
import joblib
from fastapi import HTTPException

from src.config import CHEMIN_MODELE, CHEMIN_ENCODEURS

_modele = None
_encodeurs = None


def charger_modele():
    """Charge le modèle et les encodeurs en mémoire. À appeler une fois
    au démarrage de l'application."""
    global _modele, _encodeurs
    try:
        _modele = joblib.load(CHEMIN_MODELE)
        _encodeurs = joblib.load(CHEMIN_ENCODEURS)
        print("Modèle et encodeurs chargés avec succès.")
    except FileNotFoundError as e:
        print(
            f"ATTENTION : fichier manquant ({e}). "
            f"Placez modele_prediction_ventes.pkl et encodeurs.pkl dans models/."
        )


def get_modele():
    return _modele


def get_encodeurs():
    return _encodeurs


def encoder_categorie(nom_colonne: str, valeur: str) -> int:
    """Encode une valeur catégorielle avec l'encodeur sauvegardé.
    Lève une erreur explicite si la valeur n'a jamais été vue à l'entraînement."""
    le = _encodeurs[nom_colonne]
    if valeur not in le.classes_:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Valeur inconnue pour '{nom_colonne}' : '{valeur}'. "
                f"Valeurs connues : {list(le.classes_)}"
            ),
        )
    return int(le.transform([valeur])[0])
