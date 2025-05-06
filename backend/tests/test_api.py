import json
import pytest
import requests
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, Mock, mock_open

client = TestClient(app)

# === Données de test ===
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

mock_ecoles = {
    "results": [
        {
            "position": {"lat": 47.2, "lon": -1.55},
            "code_postal_uai": "44000",
            "adresse_uai": "1 rue de l'\u00e9cole",
            "denomination_principale": "\u00c9cole \u00c9l\u00e9mentaire Jules Ferry",
            "libelle_commune": "Nantes"
        },
        {
            "position": {"lat": 47.2, "lon": -1.56},
            "code_postal_uai": "44000",
            "adresse_uai": "2 avenue du lyc\u00e9e",
            "denomination_principale": "LYCEE Cl\u00e9menceau",
            "libelle_commune": "Nantes"
        }
    ]
}

mock_etablissements = {
    "results": [
        {
            "rs": "Maison M\u00e9dicale du Centre",
            "com_code": "44109",
            "address": "10 rue de la sant\u00e9",
            "coord": {"lat": 47.2, "lon": -1.55},
            "dateouv": "2012-09-01",
            "com_name": "Nantes"
        }
    ]
}

# === Index ===


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# === Communes ===


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
    assert response.json() == {
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


@patch("requests.get")
def test_ecoles_stats_all(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_ecoles),
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
        Mock(status_code=200, json=lambda: mock_ecoles),
        Mock(status_code=200, json=lambda: {"results": []})
    ]
    response = client.get("/ecoles/stats?ville=Nantes")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_total"] == 2
    assert all(ecole["libelle_commune"].lower() ==
               "nantes" for ecole in data["données"])


@patch("requests.get", side_effect=requests.exceptions.RequestException("API HS"))
def test_ecoles_stats_api_error(mock_get):
    response = client.get("/ecoles/stats")
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Erreur lors de la récupération des données"}


@patch("requests.get")
def test_get_etablissements_success(mock_get):
    mock_get.return_value = Mock(
        status_code=200, json=lambda: mock_etablissements)
    response = client.get("/etablissements?commune=Nantes")
    assert response.status_code == 200
    data = response.json()
    assert data["commune"] == "Nantes"
    assert isinstance(data["etablissements"], list)
    assert len(data["etablissements"]) == 1
    assert data["etablissements"][0]["rs"] == "Maison M\u00e9dicale du Centre"


@patch("requests.get", side_effect=requests.exceptions.RequestException("Erreur API"))
def test_get_etablissements_api_failure(mock_get):
    response = client.get("/etablissements?commune=Nantes")
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Impossible de récupérer les établissements."}


def test_get_etablissements_missing_param():
    response = client.get("/etablissements")
    assert response.status_code == 422

# === Services: médecins ===


@patch("requests.get")
def test_compteur_medecin_with_commune(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {"nhits": 42})
    from services.medecins import compteur_medecin
    assert compteur_medecin("Nantes") == 42


@patch("requests.get")
def test_compteur_medecin_without_commune(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {"nhits": 15})
    from services.medecins import compteur_medecin
    assert compteur_medecin() == 15


@patch("requests.get", side_effect=requests.exceptions.RequestException("Erreur réseau"))
def test_compteur_medecin_exception(mock_get):
    from services.medecins import compteur_medecin
    assert compteur_medecin("Atlantis") == 0

# === POST admin update commune (mocké) ===


@patch("routes.communes.update_commune_info_file")
def test_post_update_commune(mock_update):
    response = client.post("/admin/update-commune-info")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Fichier communes_info.json mis à jour avec succès."}
    mock_update.assert_called_once()


@patch("routes.communes.update_commune_info_file", side_effect=Exception("fail"))
def test_post_update_commune_error(mock_update):
    response = client.post("/admin/update-commune-info")
    assert response.status_code == 500
    assert "Erreur lors de la mise à jour" in response.json()["detail"]
