# 🏥 Simulateur Territorial – Hackathon "Soigner le Territoire"

Ce projet a été réalisé dans le cadre du hackathon visant à lutter contre les déserts médicaux en Loire-Atlantique.

🎯 **Objectif :** Fournir aux élus un outil de simulation pour tester différents scénarios d'implantation de professionnels de santé (ex : maisons de santé, mobilité, zones prioritaires).

---

## 🧱 Architecture de l’application

| Composant | Techno      | Description                                  |
| --------- | ----------- | -------------------------------------------- |
| Frontend  | React (CRA) | Interface interactive de simulation          |
| Backend   | FastAPI     | API pour le traitement des données & calculs |

---

## 🚀 Lancement rapide (1 commande)

### ✅ Prérequis

- Python ≥ 3.9
- Node.js ≥ 16
- Unix-like shell (`bash`, compatible WSL/macOS/Linux)

### ▶️ Lancer toute l’application :

```bash
bash start.sh
```

Ce script :

- Crée les environnements virtuels
- Installe les dépendances du backend et du frontend
- Démarre l’API FastAPI sur [http://localhost:8000](http://localhost:8000)
- Démarre le frontend React sur [http://localhost:3000](http://localhost:3000)

---

## 🔧 Commandes manuelles (si besoin)

### Backend (FastAPI)

```bash
cd Hackathon/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React)

```bash
cd Hackathon/hackathon-softeam
npm install
npm start
```

---

## 🌐 URLs

- Frontend : [http://localhost:3000](http://localhost:3000)
- Backend API : [http://localhost:8000](http://localhost:8000)
- Docs API Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Structure du projet

```
Hackathon/
├── backend/              # API FastAPI
├── hackathon-softeam/    # Frontend React
└── start.sh              # Script d’installation automatique
```

## 🪵 Logs d’erreurs backend

Tous les logs d’erreurs du backend sont automatiquement enregistrés dans un fichier :

```
Hackathon/backend/logs/app.log
```

Ce fichier contient :

- Les erreurs d’exécution FastAPI/Uvicorn
- Les traces Python (exceptions)
- Les erreurs réseau/API éventuelles

Cela permet un **suivi facile des problèmes** sans avoir besoin de rester connecté au terminal.

> 💡 **Astuce développeur :** Pour observer les erreurs en temps réel, utilisez :

```bash
tail -f backend/logs/app.log
```
