import os
import requests
from fastapi import APIRouter, HTTPException, Query
from utils.logger import logger

router = APIRouter()

BASE_URL = (
    "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/"
    "234400034_etablissements-premier-et-second-degres-pdl/records"
)
SELECT_FIELDS = "position,code_postal_uai,adresse_uai,denomination_principale,libelle_commune"
DEPARTEMENT_FILTER = 'code_departement="044" and etat_etablissement=1'
LIMIT_PAR_PAGE = 100


@router.get("/ecoles/stats", tags=["Écoles"])
def stats_ecoles(ville: str = Query(default=None, description="Filtrer par nom de ville")):
    """
    Retourne les statistiques des établissements scolaires (1er et 2nd degré).
    Filtrage possible par nom de ville.
    """
    logger.info(f"Requête /ecoles/stats pour ville={ville or 'toutes'}")
    try:
        all_results = fetch_all_ecoles()

        # Filtrage optionnel par ville
        if ville:
            all_results = [
                e for e in all_results
                if e.get("libelle_commune", "").lower() == ville.lower()
            ]

        # Analyse des types d'établissements
        counts = classify_etablissements(all_results)

        return {
            "nombre_total": len(all_results),
            "répartition": counts,
            "données": all_results
        }

    except requests.exceptions.RequestException as e:
        logger.exception(
            f"Erreur lors de l'appel API établissements scolaires : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la récupération des données")


def fetch_all_ecoles() -> list:
    """
    Récupère tous les établissements scolaires du département 44 via pagination.
    """
    results = []
    offset = 0

    while True:
        params = {
            "select": SELECT_FIELDS,
            "where": DEPARTEMENT_FILTER,
            "limit": LIMIT_PAR_PAGE,
            "offset": offset
        }

        logger.debug(f"Appel API écoles avec offset={offset}")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json().get("results", [])
        if not data:
            break

        results.extend(data)
        offset += LIMIT_PAR_PAGE

    logger.info(f"{len(results)} établissements récupérés")
    return results


def classify_etablissements(data: list) -> dict:
    """
    Classe les établissements en deux catégories :
    - maternelle/élémentaire/primaire
    - collège/lycée
    """
    counts = {
        "maternelle_elementaire": 0,
        "college_lycee": 0
    }

    for ecole in data:
        denom = ecole.get("denomination_principale", "").lower()
        if any(mot in denom for mot in ["ecole", "maternelle", "élémentaire", "primaire"]):
            counts["maternelle_elementaire"] += 1
        elif any(mot in denom for mot in ["college", "lycee"]):
            counts["college_lycee"] += 1

    return counts
