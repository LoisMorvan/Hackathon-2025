import os
import json
import requests
from typing import List, Optional, Union, Dict
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ValidationError
from fastapi.params import Query as FastAPIQuery
app = FastAPI(
    title="API Communes 44",
    description="API de recherche de communes en Loire-Atlantique 🐌",
    version="1.0"
)

# === MODELES ===

class CommuneSimple(BaseModel):
    nom: str
    codesPostaux: List[str]
    population: Optional[int] = 0

class Coordonnees(BaseModel):
    lat: float
    lon: float

class CommuneBase(BaseModel):
    nom_commune: str
    code_postal: str
    population: int

class CommuneInfo(CommuneBase):
    nombre_medecins: int
    ratio: Optional[float] = None
    coordonnees: Coordonnees

# === ROUTES ===

@app.get("/", tags=["Index"])
def index() -> Dict[str, str]:
    return {"message": "API de recherche de communes en Loire-Atlantique"}

@app.get("/communes", response_model=List[CommuneSimple], tags=["Communes"])
def get_communes(value: Optional[str] = Query(None, description="Nom ou code postal (facultatif)")):
    try:
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

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"🥴 Oups, la requête a échoué : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données")


@app.get("/commune-info", response_model=Union[CommuneInfo, List[CommuneInfo]], tags=["Communes enrichies"])
def commune_info(value: Optional[str] = Query(None, description="Nom ou code postal de la commune (facultatif)")):
    try:
        # Corrige la valeur si elle est un objet Query
        if isinstance(value, FastAPIQuery):
            value = None

        file_path = os.path.join(os.getcwd(), "communes_info.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Le fichier 'communes_info.json' est introuvable. Veuillez le générer d'abord.")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        data = [CommuneInfo(**c) for c in raw_data]

        if value:
            filtered = [
                c for c in data
                if value.lower() in c.nom_commune.lower() or value in c.code_postal
            ]
            if not filtered:
                raise HTTPException(status_code=404, detail=f"Aucune commune trouvée pour '{value}'")
            return filtered[0] if len(filtered) == 1 else filtered

        return data

    except ValidationError as e:
        print(f"💥 Validation error: {e}")
        raise HTTPException(status_code=500, detail="Erreur de validation des données.")
    except Exception as e:
        print(f"📁 Erreur lecture JSON : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la lecture des données locales")

# === Fonction auxiliaire ===

def compteur_medecin(commune: Optional[str] = None) -> int:
    base_url = "https://public.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": "medecins",
        "rows": 0,
        "refine.libelle_profession": "Médecin généraliste",
        "refine.dep_name": "Loire-Atlantique"
    }
    if commune:
        params["refine.commune"] = commune

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("nhits", 0)
    except requests.RequestException as e:
        print(f"🚨 Erreur pendant l'appel API : {e}")
        return 0

# === Test local si exécution directe ===

if __name__ == "__main__":
    try:
        result = commune_info()  # ou None pour tout
        print(json.dumps(
            [r.model_dump() for r in result] if isinstance(result, list) else result.model_dump(),
            indent=2, ensure_ascii=False
        ))
    except HTTPException as e:
        print(f"Erreur : {e.detail}")
