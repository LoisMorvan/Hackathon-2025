from fastapi import APIRouter, Query, HTTPException
import requests
from utils.logger import logger

router = APIRouter()

API_BASE = "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/etablissements-du-domaine-sanitaire-et-social-2019/records"
SELECT_FIELDS = "rs,com_code,address,coord,dateouv,com_name"
CATEGORIE_PAR_DEFAUT = "Maison de santé (L.6223-3)"
DEPARTEMENT_CODE = "44"


@router.get("/etablissements", tags=["Etablissements"])
def get_etablissements_par_commune(
    commune: str = Query(..., description="Nom de la commune à rechercher"),
    categorie: str = Query(
        CATEGORIE_PAR_DEFAUT, description="Catégorie d'établissement (ex: Maison de santé)")
):
    try:
        logger.info(
            f"Recherche des établissements pour commune='{commune}', catégorie='{categorie}'")
        etablissements = fetch_etablissements(commune, categorie)
        logger.debug(
            f"{len(etablissements)} établissement(s) trouvé(s) pour {commune}")
        return {"commune": commune, "etablissements": etablissements}
    except Exception as e:
        logger.exception(
            f"Erreur lors de la récupération des établissements pour {commune}")
        raise HTTPException(
            status_code=500, detail="Impossible de récupérer les établissements.")


def fetch_etablissements(commune: str, categorie: str) -> list:
    params = {
        "select": SELECT_FIELDS,
        "refine.dep_code": DEPARTEMENT_CODE,
        "refine.libcategetab": categorie,
        "where": f'com_name="{commune}"'
    }

    response = requests.get(API_BASE, params=params)
    response.raise_for_status()

    return response.json().get("results", [])
