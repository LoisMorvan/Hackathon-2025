import pytest
from fastapi.testclient import TestClient
from main import app
import os
import json

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de recherche de communes en Loire-Atlantique"}

def test_get_communes_all():
    response = client.get("/communes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "nom" in response.json()[0]

def test_get_communes_by_name():
    response = client.get("/communes?value=Nantes")
    assert response.status_code == 200
    assert any("Nantes" in c["nom"] for c in response.json())

def test_commune_info_all(monkeypatch):
    sample_data = [{
        "nom_commune": "Nantes",
        "code_postal": "44000",
        "population": 300000,
        "nombre_medecins": 150,
        "ratio": 0.5,
        "coordonnees": {"lat": 47.218371, "lon": -1.553621}
    }]

    file_path = os.path.join(os.getcwd(), "communes_info.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f)

    response = client.get("/commune-info")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["nom_commune"] == "Nantes"

    os.remove(file_path)

def test_commune_info_by_name(monkeypatch):
    file_path = os.path.join(os.getcwd(), "communes_info.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([{
            "nom_commune": "Nantes",
            "code_postal": "44000",
            "population": 300000,
            "nombre_medecins": 150,
            "ratio": 0.5,
            "coordonnees": {"lat": 47.218371, "lon": -1.553621}
        }], f)

    response = client.get
