#!/bin/sh
set -e

git init -q

dvc remote modify origin --local auth basic
dvc remote modify origin --local user "$DAGSHUB_USER"
dvc remote modify origin --local password "$DAGSHUB_TOKEN"
dvc pull models/modele_prediction_ventes.pkl models/encodeurs.pkl

exec uvicorn app:app --host 0.0.0.0 --port 7860