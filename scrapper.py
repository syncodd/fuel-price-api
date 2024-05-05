
from url_list import URLS
from fuel_data import FuelData

import requests
import pandas as pd

class FuelPriceScrapper:

    def __init__(self):

        self.fuel_data_list = []

    def scrap_tppd(self) -> list[FuelData]:

        URL = URLS["tppd"]

        res = requests.get(URL)

        html_tables = pd.read_html(res.content)

        df = html_tables[0]

        types = df.columns[1:]

        self.fuel_data_list = []

        for district_values in df.values:

            district = district_values[0]

            for i, val in enumerate(district_values[1:]):
                self.fuel_data_list.append(
                    FuelData(
                        name=types[i],
                        district=district,
                        price=val/100,
                        unit=types[i].split(" ")[-1] if "TL" in types[i] else "",
                        source="TPPD"
                    )
                )
        
        return self.fuel_data_list

if __name__ == '__main__':

    FuelPriceScrapper().scrap_tppd()