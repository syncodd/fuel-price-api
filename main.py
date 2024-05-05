
import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.tppd.com.tr/akaryakit-fiyatlari")

import pandas as pd
html_tables = pd.read_html(res.content)
df = html_tables[0]
print(df)
