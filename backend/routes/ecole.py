import os
import requests
from fastapi import APIRouter, HTTPException, Query
from utils.logger import logger
import json
import datetime
import requests

router = APIRouter()

BASE_URL = (
    "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/"
    "234400034_etablissements-premier-et-second-degres-pdl/records"
)
SELECT_FIELDS = "position,code_postal_uai,adresse_uai,denomination_principale,libelle_commune"
DEPARTEMENT_FILTER = 'code_departement="044" and etat_etablissement=1'
LIMIT_PAR_PAGE = 100
DATA_FILE = os.path.join(os.getcwd(), "ecoles_44_.json")


@router.get("/ecoles/stats", tags=["Écoles"])
def stats_ecoles(ville: str = Query(default=None, description="Filtrer par nom de ville")):
    print("Route /ecoles/stats chargée")

    try:
        # Chemin vers le fichier généré (adapter le nom si besoin)
        fichier = DATA_FILE  # Exemple statique, tu peux automatiser selon le plus récent

        if not os.path.exists(fichier):
            raise HTTPException(
                status_code=404, detail="Fichier de données non trouvé")

        with open(fichier, "r", encoding="utf-8") as f:
            all_results = json.load(f)

        # Filtrage par ville si précisé
        if ville:
            all_results = [
                e for e in all_results
                if e.get("libelle_commune", "").lower() == ville.lower()
            ]

        # Comptage des établissements
        counts = {
            "maternelle_elementaire": 0,
            "college_lycee": 0
        }

        for ecole in all_results:
            denom = ecole.get("denomination_principale", "").lower()
            if any(mot in denom for mot in ["ecole", "maternelle", "élémentaire", "primaire"]):
                counts["maternelle_elementaire"] += 1
            elif any(mot in denom for mot in ["college", "lycee", "enseign"]):
                counts["college_lycee"] += 1

        return {
            "nombre_total": len(all_results),
            "répartition": counts,
            "données": all_results
        }

    except Exception as e:
        print(f"Erreur : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors du traitement des données locales")


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


DATA_FILE = os.path.join(os.getcwd(), "ecoles_44_.json")


@router.get("/admin/ecoles", tags=["Écoles"])
def ecoles():
    print("Route /admin/ecoles appelée")
    try:
        base_url = "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/234400034_etablissements-premier-et-second-degres-pdl/records"

        params = {
            "select": "position,code_postal_uai,adresse_uai,denomination_principale,libelle_commune",
            "where": 'code_departement="044" and etat_etablissement=1',
            "limit": 100
        }

        all_results = []
        offset = 0

        while True:
            params["offset"] = offset
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data = response.json().get("results", [])

            if not data:
                break

            all_results.extend(data)
            offset += 100

        # Génération du fichier JSON avec horodatage
        filename = "ecoles_44_.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)

        print(f"Données enregistrées dans le fichier : {filename}")
        return {"message": f"Fichier JSON généré : {filename}", "total": len(all_results)}

    except requests.exceptions.RequestException as e:
        print(f"Erreur API : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la récupération des données")
