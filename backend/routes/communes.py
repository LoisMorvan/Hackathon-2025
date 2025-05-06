import os
import json
import requests
from functools import lru_cache
from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError
from models.commune import CommuneSimple, CommuneInfo
from services.medecins import compteur_medecin
from utils.logger import logger

router = APIRouter()

DATA_FILE = os.path.join(os.getcwd(), "communes_info.json")


@router.get("/communes", response_model=List[CommuneSimple], tags=["Communes"])
def get_communes(value: Optional[str] = Query(None, description="Nom ou code postal (facultatif)")):
    """
    Retourne une liste de communes de Loire-Atlantique,
    filtrées par nom ou code postal si un paramètre est fourni.
    """
    try:
        logger.info(f"Requête /communes avec filtre: {value}")
        url, params = build_commune_api_request(value)

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.exception(f"Erreur récupération des communes : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la récupération des données")


@router.get("/commune-info", response_model=Union[CommuneInfo, List[CommuneInfo]], tags=["Communes enrichies"])
def commune_info(value: Optional[str] = Query(None, description="Nom ou code postal de la commune (facultatif)")):
    """
    Retourne les informations enrichies (population, médecins, coordonnées)
    pour une ou plusieurs communes stockées dans un fichier JSON.
    """
    try:
        logger.info(f"Requête /commune-info avec filtre: {value}")
        if not os.path.exists(DATA_FILE):
            raise HTTPException(
                status_code=500, detail="Le fichier 'communes_info.json' est introuvable. Veuillez le générer d'abord.")

        data = get_cached_commune_info()

        if value:
            filtered = [
                c for c in data
                if value.lower() in c.nom_commune.lower() or value in c.code_postal
            ]
            if not filtered:
                raise HTTPException(
                    status_code=404, detail=f"Aucune commune trouvée pour '{value}'")
            return filtered[0] if len(filtered) == 1 else filtered

        return data

    except ValidationError as e:
        logger.exception(f"Erreur validation Pydantic : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur de validation des données.")
    except Exception as e:
        logger.exception(f"Erreur lecture JSON : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la lecture des données locales")


@lru_cache(maxsize=1)
def get_cached_commune_info() -> List[CommuneInfo]:
    """
    Charge et met en cache le contenu de communes_info.json pour éviter les lectures disque répétées.
    """
    logger.debug("Chargement des données communes_info.json en cache")
    return load_commune_info_file(DATA_FILE)


def update_commune_info_file() -> None:
    """
    Met à jour le fichier communes_info.json avec les données depuis l'API officielle
    et ajoute le nombre de médecins pour chaque commune.
    """
    try:
        logger.info("Mise à jour du fichier communes_info.json en cours...")
        url = "https://geo.api.gouv.fr/departements/44/communes"
        params = {"fields": "nom,codesPostaux,population,centre", "format": "json"}

        response = requests.get(url, params=params)
        response.raise_for_status()
        raw_data = response.json()

        enriched_data = []
        for c in raw_data:
            nb_medecins = compteur_medecin(c["nom"])
            enriched_data.append({
                "nom_commune": c["nom"],
                "code_postal": ", ".join(c["codesPostaux"]),
                "population": c.get("population", 0),
                "nombre_medecins": nb_medecins,
                "ratio": round(c.get("population", 0) / nb_medecins, 2) if nb_medecins else None,
                "coordonnees": {
                    "lat": c["centre"]["coordinates"][1],
                    "lon": c["centre"]["coordinates"][0]
                }
            })

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(enriched_data, f, ensure_ascii=False, indent=2)

        get_cached_commune_info.cache_clear()
        logger.info("Fichier communes_info.json mis à jour avec succès.")

    except Exception as e:
        logger.exception(f"Échec mise à jour communes_info.json : {e}")
        raise


def build_commune_api_request(value: Optional[str]) -> tuple[str, dict]:
    """
    Construit l’URL et les paramètres pour l’appel à l’API Geo.
    """
    if value is None:
        url = "https://geo.api.gouv.fr/departements/44/communes"
        params = {"fields": "nom,codesPostaux,population", "format": "json"}
    else:
        url = "https://geo.api.gouv.fr/communes"
        key = "codePostal" if value.isdigit() else "nom"
        params = {
            "fields": "nom,codesPostaux,population",
            "format": "json",
            key: value
        }
    return url, params


def load_commune_info_file(path: str) -> List[CommuneInfo]:
    """
    Charge le fichier JSON contenant les données enrichies sur les communes.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return [CommuneInfo(**entry) for entry in raw_data]
