
from dataclasses import dataclass

@dataclass
class FuelData:

    name: str
    district: str
    price: float
    unit: str
    source: str