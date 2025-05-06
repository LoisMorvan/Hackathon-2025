### 📘 README – Backend Hackathon

> API FastAPI pour la simulation d’accès aux soins en Loire-Atlantique

---

## 🚀 Lancer le backend

### Prérequis

- Python 3.9+
- pip

---

### 🔧 Installation & démarrage (développement)

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le serveur
uvicorn main:app --reload
```

Par défaut, l’API sera accessible sur :
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)
👉 Docs Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Lancer les tests

```bash
pytest
```

---

## 📁 Structure

```txt
backend/
├── main.py              # Entrée FastAPI
├── requirements.txt     # Dépendances
├── tests/               # (optionnel) Dossier de tests
└── README.md            # Ce fichier
```
