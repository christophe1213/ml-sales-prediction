"""
Schémas Pydantic : validation des requêtes et réponses de l'API.
"""
from pydantic import BaseModel, ConfigDict, Field


class DemandePrediction(BaseModel):
    store_nbr: int = Field(..., description="Numéro du magasin (ex. 1)")
    family: str = Field(..., description="Famille de produit (ex. 'GROCERY I')")
    onpromotion: int = Field(0, description="Nombre de produits en promotion")
    city: str = Field(..., description="Ville du magasin")
    state: str = Field(..., description="État/région du magasin")
    type: str = Field(..., description="Type de magasin (ex. 'A', 'B'...)")
    cluster: int = Field(..., description="Cluster du magasin (regroupement Favorita)")
    dcoilwtico: float = Field(..., description="Prix du pétrole ce jour-là")
    est_ferie: int = Field(0, description="1 si jour férié national, sinon 0")
    date: str = Field(..., description="Date de la prédiction, format AAAA-MM-JJ")
    ventes_lag_7: float = Field(..., description="Ventes il y a 7 jours")
    ventes_lag_14: float = Field(..., description="Ventes il y a 14 jours")
    ventes_lag_30: float = Field(..., description="Ventes il y a 30 jours")
    ventes_mm_7: float = Field(..., description="Moyenne mobile des ventes sur 7 jours")
    ventes_mm_30: float = Field(..., description="Moyenne mobile des ventes sur 30 jours")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "store_nbr": 1,
                "family": "GROCERY I",
                "onpromotion": 5,
                "city": "Quito",
                "state": "Pichincha",
                "type": "D",
                "cluster": 13,
                "dcoilwtico": 65.5,
                "est_ferie": 0,
                "date": "2017-08-15",
                "ventes_lag_7": 1200.0,
                "ventes_lag_14": 1150.0,
                "ventes_lag_30": 1100.0,
                "ventes_mm_7": 1180.0,
                "ventes_mm_30": 1120.0,
            }
        }
    )


class ReponsePrediction(BaseModel):
    ventes_predites: float
