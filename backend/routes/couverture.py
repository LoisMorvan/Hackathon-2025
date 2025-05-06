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
        raise HTTPException(status_code=500, detail="Fichier de données introuvable.")
    except json.JSONDecodeError:
        logger.error("Erreur de décodage JSON")
        raise HTTPException(status_code=500, detail="Erreur de lecture des données JSON.")

    total = len(communes)
    if total == 0:
        return {"message": "Aucune commune trouvée."}

    # Comptage
    plus_de_3_3 = sum(1 for c in communes if c.get("ratio", 0) > 3.3)
    entre_2_et_3_3 = sum(1 for c in communes if 2 <= c.get("ratio", 0) <= 3.3)
    moins_de_2 = sum(1 for c in communes if c.get("ratio", 0) < 2)

    # Pourcentage
    def pourcentage(valeur): return round((valeur / total) * 100, 2)

    return {
        "bonne": f"{pourcentage(plus_de_3_3)}%",
        "moyenne": f"{pourcentage(entre_2_et_3_3)}%",
        "sous-dote": f"{pourcentage(moins_de_2)}%"
    }
