
from utils.fuel_price_scrapper.url_list import URLS
from utils.fuel_price_scrapper.fuel_data import FuelData

import math
import requests
import pandas as pd

class FuelPriceScrapper:

    def __init__(self):

        self.fuel_data_list = []
        self.fuel_data_list: list[FuelData]

    def scrap_base(self, url) -> pd.DataFrame:

        res = requests.get(url)

        html_tables = pd.read_html(res.content)

        df = html_tables[0]

        return df
    
    def scrap_tppd(self) -> list[FuelData]:

        URL = URLS.get("tppd")

        if not URL: return

        df = self.scrap_base(URL)

        types = df.columns[1:]

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
    
    def scrap_po(self) -> list[FuelData]:

        URL = URLS.get("po")

        if not URL: return

        df = self.scrap_base(URL)

        types = df.columns[1:]

        for district_values in df.values:

            district = district_values[0]

            for i, val in enumerate(district_values[1:]):
                self.fuel_data_list.append(
                    FuelData(
                        name=types[i],
                        district=district,
                        price=float(val.split(' ')[0]),
                        unit=val.split(' ')[-3] if "TL" in val else "",
                        source="PO"
                    )
                )

        return self.fuel_data_list

    def scrap(self):

        self.scrap_tppd()
        self.scrap_po()
    
    def get_avg_by_district_and_name(self, district="", name=[]):

        price_list = [fuel_price.price for fuel_price in self.fuel_data_list if fuel_price.is_district_in(district) and fuel_price.is_name_in(name)]
        
        return 0 if len(price_list) == 0 else sum(price_list) / len(price_list)


if __name__ == '__main__':

    scrapper = FuelPriceScrapper()

    scrapper.scrap()
    print(scrapper.get_avg_by_district_and_name("istanbul", ["KURŞUNSUZ BENZİN (TL/LT)",
                                                             "V/Max Kurşunsuz 95"]))
