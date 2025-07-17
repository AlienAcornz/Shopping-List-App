from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path

driverPath = Path(__file__).parent / "chromedriver.exe"

service = Service(executable_path=driverPath)
driver = webdriver.Chrome(service=service)

driver.get('https://www.aldi.co.uk/products/fresh-food/vegetables/k/1588161416978050002?sort=name_asc&page=1')
time.sleep(5)
doc = BeautifulSoup(driver.page_source, 'html.parser')
item_grid = doc.select_one('.product-grid')
items = item_grid.find_all(class_='product-tile')

for item in items:
    if item.find(class_="product-tile__picture").img.get('loading') == 'lazy': # skip the item if it is being pre-loaded
        continue
    name = item.find(class_='product-tile__name').p.get_text(strip=True)
    price = item.find(class_='base-price__comparison-price').span.get_text(strip=True)
    print(name, price)