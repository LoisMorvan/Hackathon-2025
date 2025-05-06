from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import index, communes, etablissements,couverture,ecole


app = FastAPI(
    title="API Communes 44",
    description="API de recherche de communes en Loire-Atlantique 🐌",
    version="1.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Autorise uniquement cette origine
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

# Inclusion des routes
app.include_router(index.router)
app.include_router(communes.router)
app.include_router(etablissements.router)
app.include_router(couverture.router)
app.include_router(ecole.router)
