import urllib
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI(
    title="API Communes 44",
    description="API de recherche de communes en Loire-Atlantique 🐌",
    version="1.0"
)


@app.get("/", tags=["Index"])
def index():
    return {"message": "API de recherche de communes en Loire-Atlantique"}


@app.get("/communes", tags=["Communes"])
def get_communes(value: str = Query(None, description="Nom ou code postal (facultatif)")):
    try:
        if value is None:
            url = "https://geo.api.gouv.fr/departements/44/communes"
            params = {"fields": "nom,codesPostaux,population", "format": "json"}
        else:
            url = "https://geo.api.gouv.fr/communes"
            params = {
                "fields": "nom,codesPostaux,population",
                "format": "json",
                "codePostal" if value.isdigit() else "nom": value
            }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"🥴 Oups, la requête a échoué : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données")


@app.get("/commune-info", tags=["Communes enrichies"])
def commune_info(value: str = Query(None, description="Nom ou code postal de la commune (facultatif)")):
    try:
        if value is None:
            url = "https://geo.api.gouv.fr/departements/44/communes"
            params = {"fields": "nom,codesPostaux,population,centre", "format": "json"}
            response = requests.get(url, params=params)
            response.raise_for_status()
            communes = response.json()
        else:
            url = "https://geo.api.gouv.fr/communes"
            params = {
                "fields": "nom,codesPostaux,population,centre",
                "format": "json",
                "codePostal" if value.isdigit() else "nom": value
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            communes = response.json()
            if not communes:
                raise HTTPException(status_code=404, detail=f"Aucune commune trouvée pour '{value}'")

        results = []
        for commune in communes:
            nom = commune["nom"]
            codes_postaux = ", ".join(commune["codesPostaux"])
            population = commune.get("population", 0)
            lat = commune["centre"]["coordinates"][1]
            lon = commune["centre"]["coordinates"][0]
            nb_medecins = compteur_medecin(nom)

            result = {
                "nom_commune": nom,
                "code_postal": codes_postaux,
                "population": population,
                "nombre_medecins": nb_medecins,
                "ration": round(population / nb_medecins, 2) if nb_medecins else None,
                "coordonnees": {
                    "lat": lat,
                    "lon": lon
                }
            }
            results.append(result)

        return results if value is None else results[0]

    except requests.exceptions.RequestException as e:
        print(f"🧨 Erreur API : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données")


def compteur_medecin(commune: str = None) -> int:
    base_url = (
        "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/medecins/records"
        "?limit=1"
    )

    filtres = [
        "refine=libelle_profession%3A%22Médecin%20généraliste%22",
        "refine=dep_name%3A%22Loire-Atlantique%22"
    ]

    if commune:
        commune_filtrée = urllib.parse.quote(commune)
        filtres.append(f"refine=commune%3A%22{commune_filtrée}%22")

    url = base_url + "&" + "&".join(filtres)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("total_count", 0)
    except requests.RequestException as e:
        print(f"🧨 Erreur pendant l'appel API : {e}")
        return 0
