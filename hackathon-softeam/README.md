### 📘 README – Frontend Hackathon

> Interface de simulation pour améliorer l'accès aux soins en Loire-Atlantique
> Technologies : React (Create React App), ApexCharts, Axios

---

## 🚀 Lancer le projet

### Prérequis

* Node.js ≥ 16.x
* npm ≥ 8.x (ou Yarn si préféré)

---

### 🧪 Environnement de développement

```bash
# 1. Installation des dépendances
npm install

# 2. Lancer le serveur local (http://localhost:3000)
npm start
```

---

### 🏗️ Build production

```bash
# Génération des fichiers optimisés dans /build
npm run build
```

---

### 🧪 Tests

```bash
npm test
```

---

### 📁 Structure du projet

```txt
hackathon-softeam/
├── public/             # Fichiers statiques
├── src/                # Code source React
│   ├── components/     # Composants UI
│   ├── pages/          # Pages principales
│   ├── assets/         # Images et styles
│   └── App.js          # Entrée principale
├── package.json        # Dépendances & scripts
└── README.md           # Ce fichier
```

---

## 🧠 Notes techniques

* Utilise **Axios** pour communiquer avec l'API
* Visualisation interactive avec **ApexCharts**
* Typage facilité avec `@types/react`, `@types/node`, etc.
* Peut être couplé à un backend Node ou une API tierce REST