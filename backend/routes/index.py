from fastapi import APIRouter, Request
from utils.logger import logger

router = APIRouter()


@router.get("/", tags=["Index"])
def index(request: Request):
    """
    Endpoint racine de l'API.
    Fournit une description générale et les principales routes disponibles.
    """
    client_host = request.client.host if request.client else "inconnu"
    logger.info(f"Accès à la racine de l’API depuis {client_host}")

    return {
        "message": "Bienvenue sur l'API de recherche de communes en Loire-Atlantique",
        "version": "1.0",
        "endpoints": {
            "/communes": "Recherche simple par nom ou code postal",
            "/commune-info": "Infos enrichies : population, médecins, localisation",
            "/etablissements": "Maisons de santé par commune"
        },
        "documentation": "/docs",
        "auteur": "Hackathon Santé - Équipe Loire-Atlantique"
    }
