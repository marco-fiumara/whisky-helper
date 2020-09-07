from bs4 import BeautifulSoup
import requests
from typing import List
import json
import time


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def GetAllWhiskeys(urls: List[str]) -> dict:
    links = {}
    for url in urls:
        print(f"Starting {url}")
        page_count = 0
        for page in url:
            if page_count == 0 or page_count > 1:
                print(f"Processing page {page_count}...")
                req = requests.get(f"{url}/{page_count if page_count > 1 else ''}", headers)
                soup = BeautifulSoup(req.content, 'html.parser')

                try:
                    content = soup.find("div", id="productBoxWideContainer")
                except AttributeError:
                    break

                try:
                    rows = list(content.find_all("div", class_="boxBgr product-box-wide h-gutter js-product-box-wide"))
                except AttributeError:
                    break

                for row in rows:
                    query = row.find("h3")
                    h3 = query.get_text()
                    link = query.find("a").get('href')
                    links[h3] = link

            print(f"Processed page {page_count}!")
            page_count += 1
        print(f"Finished {url}")

    return links


years: List[str] = ["https://www.masterofmalt.com/age/10-year-old-whisky",
                    "https://www.masterofmalt.com/age/12-year-old-whisky", "https://www.masterofmalt.com/age/18-year-old-whisky", "https://www.masterofmalt.com/age/21-year-old-whisky"]

# result: dict = GetAllWhiskeys(years)

# with open('whiskeys_output.json', 'w') as parsed_data:
#     json.dump(result, parsed_data)

data: dict = {}


start = time.time()
with open('whiskeys_output.json', 'r') as whisky_output:
    whisky_data = json.load(whisky_output)
    # whisky_data = result

    for whisky in whisky_data:
        if whisky in data:
            print(f"{whisky} already exists")
        else:
            try:
                print(f"Scraping {whisky} info...")
                req = requests.get(f"{whisky_data[whisky]}", headers)
                soup = BeautifulSoup(req.content, 'html.parser')

                title = soup.find("h1", id='ContentPlaceHolder1_pageH1').get_text()

                initial_image = soup.find("div", id='imgProductBigDiv').find("div", class_='productImageWrap').find("img").get("src")

                image = "".join(initial_image[2:])

                # Attempt to get Varietal (Country)
                try:
                    varietal = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdCountry').find("span", class_='kv-val').find("a").get_text()
                except AttributeError:
                    # Attempt to get Varietal (Country) with alternative id value
                    try:
                        varietal = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl01_wdCountry').find("span", class_='kv-val').find("a").get_text()
                    except AttributeError:
                        varietal = ""

                # Attempt to get Region
                try:
                    region = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdRegion').find("span", class_='kv-val').find("a").get_text()
                except AttributeError:
                    # Attempt to get Region with alternative id value
                    try:
                        region = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl01_wdRegion').find("span", class_='kv-val').find("a").get_text()
                    except AttributeError:
                        region = ""

                # Attempt to get Brand
                try:
                    brand = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdDistillery').find("span", class_='kv-val').find("a").get_text()
                except AttributeError:
                    # Attempt to get Brand with alternative id value
                    try:
                        brand = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl01_wdDistillery').find("span", class_='kv-val').find("a").get_text()
                    except AttributeError:
                        brand = ""

                # Attempt to get Age
                try:
                    age = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdYearsMatured').find("span", class_='kv-val').find("a").get_text()
                except AttributeError:
                    # Attempt to get Age with alternative id value
                    try:
                        age = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl01_wdYearsMatured').find("span", class_='kv-val').find("a").get_text()
                    except AttributeError:
                        age = ""

                # Attempt to get Style
                try:
                    style = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdStyle').find("span", class_='kv-val').find("a").get_text()
                except AttributeError:
                    # Attempt to get Style with alternative id value
                    try:
                        style = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdStyle').find("span", class_='kv-val').find("a").get_text()
                    except AttributeError:
                        style = ""

                # Attempt to get Alcohol Percentage
                try:
                    alcohol_percentage = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdAlcohol').find("span", class_='kv-val').get_text()
                except AttributeError:
                    # Attempt to get Alcohol Percentage with alternative id value
                    try:
                        alcohol_percentage = soup.find("div", id='ContentPlaceHolder1_ctl00_ctl00_wdAlcohol').find("span", class_='kv-val').get_text()
                    except AttributeError:
                        alcohol_percentage = ""

                data[title] = {
                    "Country": "",
                    "Image": image,
                    "Varietal": varietal,
                    "Region": region,
                    "Whisky Style": style,
                    "Brand Name": brand,
                    "Name": title,
                    "Age": age,
                    "Alcohol Volume (%)": alcohol_percentage,
                    "Price ($ per bottle)": None,
                    "Peated (Y/N)": None,
                    "Rating ( /10)": None}

                # print(data)
                print(f"Scraped {whisky}!")
            except AttributeError:
                print(f"Error on: {whisky}")
                continue


with open('whiskeys_new_output.json', 'w') as whisky_new_output:
    json.dump(data, whisky_new_output)

end = time.time()

print(f"Time taken: {end - start}s")

# url = "https://www.masterofmalt.com/age/10-year-old-whisky/"

# req = requests.get(url, headers)

# soup = BeautifulSoup(req.content, 'html.parser')

# content = soup.find("div", id="productBoxWideContainer")

# rows = list(content.find_all("div", class_="boxBgr product-box-wide h-gutter js-product-box-wide"))

# links = {}

# for row in rows:
#     query = row.find("h3")
#     h3 = query.get_text()
#     link = query.find("a").get('href')
#     links[h3] = link
# print(h3, link)
# print(row.find("h3").prettify())
