#!/bin/sh
set -e

git init -q

echo "DAGSHUB_USER défini : ${DAGSHUB_USER:+oui}"
echo "DAGSHUB_TOKEN défini : ${DAGSHUB_TOKEN:+oui}"
echo "HELLO"
dvc remote modify origin --local auth basic
dvc remote modify origin --local user "$DAGSHUB_USER"
dvc remote modify origin --local password "$DAGSHUB_TOKEN"
dvc pull models/modele_prediction_ventes.pkl models/encodeurs.pkl

exec uvicorn app:app --host 0.0.0.0 --port 7860