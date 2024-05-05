
from dataclasses import dataclass

@dataclass
class FuelData:

    name: str
    district: str
    price: float
    unit: str
    source: str

    def is_district_in(self, district="") -> bool:
        return bool(district.upper() in self.district.upper())
    
    def is_name_in(self, name=[]) -> bool:
        return bool(self.name in name)