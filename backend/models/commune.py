from typing import List, Optional
from pydantic import BaseModel


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
