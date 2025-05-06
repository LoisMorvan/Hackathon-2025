import pytest
from fastapi.testclient import TestClient
from main import app
import os
import json
import requests
client = TestClient(app)
from unittest.mock import mock_open, patch

sample_data = json.dumps([{
    "nom_commune": "Nantes",
    "code_postal": "44000",
    "population": 300000,
    "nombre_medecins": 150,
    "ratio": 0.5,
    "coordonnees": {"lat": 47.218371, "lon": -1.553621}
}])

sample_data1 = json.dumps([
    {"nom_commune": "A", "ratio": 3.5},
    {"nom_commune": "B", "ratio": 2.5},
    {"nom_commune": "C", "ratio": 1.0}
])

def test_index():
    response = client.get("/")
    assert response.status_code == 200

def test_get_communes_all():
    response = client.get("/communes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "nom" in response.json()[0]

def test_get_communes_by_name():
    response = client.get("/communes?value=Nantes")
    assert response.status_code == 200
    assert any("Nantes" in c["nom"] for c in response.json())

@patch("builtins.open", new_callable=mock_open, read_data=sample_data)
@patch("os.path.exists", return_value=True)
def test_commune_info_all(mock_exists, mock_file):
    response = client.get("/commune-info")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["nom_commune"] == "Nantes"

@patch("builtins.open", new_callable=mock_open, read_data=sample_data)
@patch("os.path.exists", return_value=True)
def test_commune_info_by_name(mock_exists, mock_file):
    response = client.get("/commune-info?value=nantes")
    assert response.status_code == 200
    assert response.json()["nom_commune"].lower() == "nantes"

@patch("builtins.open", new_callable=mock_open, read_data=sample_data1)
@patch("os.path.exists", return_value=True)
def test_get_couvertures(mock_exists, mock_file):
    response = client.get("/couvertures")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data == {
        "bonne": "33.33%",
        "moyenne": "33.33%",
        "sous-dote": "33.33%"
    }

@patch("builtins.open", new_callable=mock_open, read_data="truc pas json")
@patch("os.path.exists", return_value=True)
def test_get_couvertures_invalid_json(mock_exists, mock_file):
    response = client.get("/couvertures")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erreur de lecture des données JSON."}

@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("os.path.exists", return_value=True)
def test_get_couvertures_empty_file(mock_exists, mock_file):
    response = client.get("/couvertures")
    assert response.status_code == 200
    assert response.json() == {"message": "Aucune commune trouvée."}

from unittest.mock import patch, Mock

mock_api_response = {
    "results": [
        {
            "position": {"lat": 47.2, "lon": -1.55},
            "code_postal_uai": "44000",
            "adresse_uai": "1 rue de l'école",
            "denomination_principale": "École Élémentaire Jules Ferry",
            "libelle_commune": "Nantes"
        },
        {
            "position": {"lat": 47.2, "lon": -1.56},
            "code_postal_uai": "44000",
            "adresse_uai": "2 avenue du lycée",
            "denomination_principale": "LYCEE Clémenceau",
            "libelle_commune": "Nantes"
        }
    ]
}

@patch("requests.get")
def test_ecoles_stats_all(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_api_response),
        Mock(status_code=200, json=lambda: {"results": []})
    ]

    response = client.get("/ecoles/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_total"] == 2
    assert data["répartition"]["maternelle_elementaire"] == 1
    assert data["répartition"]["college_lycee"] == 1

@patch("requests.get")
def test_ecoles_stats_filtered(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_api_response),
        Mock(status_code=200, json=lambda: {"results": []})
    ]

    response = client.get("/ecoles/stats?ville=Nantes")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_total"] == 2
    assert all(ecole["libelle_commune"].lower() == "nantes" for ecole in data["données"])

@patch("requests.get", side_effect=requests.exceptions.RequestException("API HS"))
def test_ecoles_stats_api_error(mock_get):
    response = client.get("/ecoles/stats")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erreur lors de la récupération des données"}

mock_api_response1 = {
    "results": [
        {
            "rs": "Maison Médicale du Centre",
            "com_code": "44109",
            "address": "10 rue de la santé",
            "coord": {"lat": 47.2, "lon": -1.55},
            "dateouv": "2012-09-01",
            "com_name": "Nantes"
        }
    ]
}

@patch("requests.get")
def test_get_etablissements_success(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: mock_api_response1)

    response = client.get("/etablissements?commune=Nantes")
    assert response.status_code == 200
    data = response.json()
    assert data["commune"] == "Nantes"
    assert isinstance(data["etablissements"], list)
    assert len(data["etablissements"]) == 1
    assert data["etablissements"][0]["rs"] == "Maison Médicale du Centre"

@patch("requests.get", side_effect=requests.exceptions.RequestException("Erreur API"))
def test_get_etablissements_api_failure(mock_get):
    response = client.get("/etablissements?commune=Nantes")
    assert response.status_code == 500
    assert response.json() == {"detail": "Impossible de récupérer les établissements."}

def test_get_etablissements_missing_param():
    response = client.get("/etablissements")
    assert response.status_code == 422  # Unprocessable Entity (paramètre obligatoire manquant)


