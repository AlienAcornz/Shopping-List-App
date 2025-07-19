from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path
import json
from mongo_client import appendPrices
import asyncio

parentDir = Path(__file__).parent

pagesToScrape = parentDir / "pages_to_scrape.json"
with open(pagesToScrape, 'r') as f:
    pages = json.load(f) #loads the websites that we want to scrape from a json filled with links

driverPath = parentDir / "chromedriver.exe"

service = Service(executable_path=driverPath)
driver = webdriver.Chrome(service=service)


for category, links in pages.items():
    price_dataframe = pd.DataFrame(columns=["name", "price", "unit", "category"]) # creates a dataframe for the info to be stored in
    for link in links:
        running = True
        index = 1
        while running:
            driver.get(f'{link}?sort=name_asc&page={index}')
            time.sleep(3)
            doc = BeautifulSoup(driver.page_source, 'html.parser')
            item_grid = doc.select_one('.product-grid')

            if not item_grid or not item_grid.find_all(recursive=False): #if there are no items being displayed on the page, exit out of the loop
                running = False
                break
            items = item_grid.find_all(class_='product-tile')

            for item in items:
                try:
                    name = item.find(class_='product-tile__name').p.get_text(strip=True).lower()
                    price_info = item.find(class_='base-price__comparison-price').span.get_text(strip=True) # looks like this: (£1.58/1 KG)
                    split_message = price_info[1:-1].split("/") #removes brackets and splits at the /
                    price = float(split_message[0].replace("£",""))  # removes the £ from the price
                    unit = split_message[1].split(" ")[1].lower() #removes the empty space in the price and selects the unit
                    price_dataframe.loc[len(price_dataframe)] = [name, price, unit, category] #appends the info to the end of the data frame
                except AttributeError: #Some random items do not have a price / kg.
                    continue
            
            index += 1
    asyncio.run(appendPrices(price_dataframe.to_dict(orient="records")))
    print(category, "Has been added to the database")
    print(price_dataframe.head())