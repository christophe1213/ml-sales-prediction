"""
Configuration centralisée : chemins des fichiers et constantes du projet.
"""
import os

# Racine du projet (dossier parent de src/)
RACINE_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHEMIN_MODELE = os.path.join(RACINE_PROJET, "models", "modele_prediction_ventes.pkl")
CHEMIN_ENCODEURS = os.path.join(RACINE_PROJET, "models", "encodeurs.pkl")

# Ordre exact des colonnes attendu par le modèle entraîné
FEATURES = [
    "store_nbr", "family", "onpromotion",
    "city", "state", "type", "cluster",
    "dcoilwtico", "EstFerie",
    "Annee", "Mois", "Jour", "JourSemaine", "Semaine", "FinDeMois",
    "Ventes_Lag_7", "Ventes_Lag_14", "Ventes_Lag_30",
    "Ventes_MM_7", "Ventes_MM_30",
]
