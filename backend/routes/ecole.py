import os
import json

import requests
from fastapi import APIRouter, HTTPException, Query
from utils.logger import logger
import requests

router = APIRouter()

@router.get("/ecoles/stats", tags=["Écoles"])
def stats_ecoles(ville: str = Query(default=None, description="Filtrer par nom de ville")):
    print("Route /ecoles/stats chargée")
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
            if any(mot in denom for mot in ["ecole", "maternelle", "élémentaire","primaire"]):
                counts["maternelle_elementaire"] += 1
            elif any(mot in denom for mot in ["college", "lycee"]):
                counts["college_lycee"] += 1

        return {
            "nombre_total": len(all_results),
            "répartition": counts,
            "données": all_results
        }

    except requests.exceptions.RequestException as e:
        print(f"📡 Erreur API : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données")