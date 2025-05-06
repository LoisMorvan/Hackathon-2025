from fastapi import FastAPI
from routes import index, communes, etablissements,couverture,ecole

app = FastAPI(
    title="API Communes 44",
    description="API de recherche de communes en Loire-Atlantique 🐌",
    version="1.0"
)

# Inclusion des routes
app.include_router(index.router)
app.include_router(communes.router)
app.include_router(etablissements.router)
app.include_router(couverture.router)
app.include_router(ecole.router)
