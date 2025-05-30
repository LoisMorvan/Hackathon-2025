#!/bin/bash

echo "🚀 Initialisation de l'application..."

# === BACKEND ===
echo "📦 Installation des dépendances backend..."
cd backend || exit 1
pip install -r requirements.txt

# Lancer le backend en arrière-plan
echo "🟢 Démarrage du backend FastAPI sur http://localhost:8000"
python -m uvicorn main:app --reload &

# Retour au dossier racine avant de passer au frontend
cd ..

# === FRONTEND ===
echo "📦 Installation des dépendances frontend..."
cd hackathon-softeam || exit 1
npm install

# Lancer le frontend
echo "🟢 Démarrage du frontend React sur http://localhost:3000"
npm start
