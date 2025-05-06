import requests
from typing import Optional
from utils.logger import logger

BASE_URL = "https://public.opendatasoft.com/api/records/1.0/search/"
DATASET = "medecins"
PROFESSION = "Médecin généraliste"
DEPARTEMENT = "Loire-Atlantique"


def compteur_medecin(commune: Optional[str] = None) -> int:
    """
    Récupère le nombre de médecins généralistes pour une commune donnée (ou l'ensemble du département 44 si non spécifiée).

    Args:
        commune (Optional[str]): Nom de la commune

    Returns:
        int: Nombre de médecins généralistes trouvés (via nhits)
    """
    params = {
        "dataset": DATASET,
        "rows": 0,
        "refine.libelle_profession": PROFESSION,
        "refine.dep_name": DEPARTEMENT
    }

    if commune:
        params["refine.commune"] = commune
        logger.debug(f"Recherche du nombre de médecins à {commune}")
    else:
        logger.debug(
            "Recherche du nombre total de médecins en Loire-Atlantique")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        count = data.get("nhits", 0)
        logger.info(
            f"{count} médecin(s) trouvé(s) pour {commune or 'tout le 44'}")
        return count
    except requests.RequestException as e:
        logger.exception(
            f"Erreur lors de la récupération des médecins pour {commune or 'département'} : {e}")
        return 0
