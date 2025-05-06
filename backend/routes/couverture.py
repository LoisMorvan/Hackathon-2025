import os
import json
from fastapi import APIRouter, HTTPException
from utils.logger import logger

router = APIRouter()

DATA_FILE = os.path.join(os.getcwd(), "communes_info.json")


@router.get("/couvertures", tags=["Couvertures"])
def get_couvertures():
    """
    Retourne les pourcentages de couverture médicale des communes,
    selon trois tranches de ratio : > 3.3, entre 2 et 3.3, et < 2.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            communes = json.load(f)
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {DATA_FILE}")
        raise HTTPException(
            status_code=500, detail="Fichier de données introuvable.")
    except json.JSONDecodeError:
        logger.error("Erreur de décodage JSON")
        raise HTTPException(
            status_code=500, detail="Erreur de lecture des données JSON.")

    total = len(communes)
    if total == 0:
        logger.warning("Aucune commune trouvée dans le fichier.")
        return {"message": "Aucune commune trouvée."}

    # Comptage des tranches
    counts = {
        "bonne": sum(1 for c in communes if c.get("ratio", 0) > 3.3),
        "moyenne": sum(1 for c in communes if 2 <= c.get("ratio", 0) <= 3.3),
        "sous-dote": sum(1 for c in communes if c.get("ratio", 0) < 2)
    }

    logger.debug(f"Répartition des tranches : {counts}")

    # Conversion en pourcentages
    pourcentages = {
        tranche: f"{round((nb / total) * 100, 2)}%"
        for tranche, nb in counts.items()
    }

    logger.info("Statistiques de couverture médicale calculées avec succès.")
    return pourcentages
