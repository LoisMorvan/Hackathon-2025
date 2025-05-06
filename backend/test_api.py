import pytest
from fastapi.testclient import TestClient
from main import app
import os
import json

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
