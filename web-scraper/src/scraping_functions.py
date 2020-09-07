from bs4 import BeautifulSoup
import requests
from typing import List, Dict
import json
import time


def get_all_whiskys(urls: List[str], headers: Dict[str, str]) -> Dict[str, str]:
    """Function to scrape name and further details link from each row of whisky from every page on each url in a list of urls from masterofmalt.com

    Args:
        urls (List[str]): urls list
        headers (Dict[str, str]): necessary Beautifulsoup4 headers

    Returns:
        dict: returns a dict of whisky name and link to full page of details
    """

    # Initialise empty dict
    links: Dict[str, str] = {}

    # Begin loop over url list
    for url in urls:
        print(f"Starting {url}")

        # Initialise page_count variable
        page_count: int = 1

        # Start while loop to go over every page from each url
        while True:
            # Start at page 1 and go till end
            if page_count >= 1:
                print(f"Processing page {page_count}...")

                # Beautifulsoup4 request url and soup init
                req = requests.get(f"{url}/{page_count}", headers)
                soup = BeautifulSoup(req.content, 'html.parser')

                # Test to see if page count has been exceeded
                try:
                    content = soup.find("div", id="productBoxWideContainer")
                except AttributeError:
                    break

                # Test to see if page count has been exceeded
                try:
                    rows = list(content.find_all(
                        "div", class_="boxBgr product-box-wide h-gutter js-product-box-wide"))
                except AttributeError:
                    break

                # If page_count is within total pages, loop over rows and add
                # title of whisky and link to more details page to dict
                for row in rows:
                    query = row.find("h3")
                    h3 = query.get_text()
                    link = query.find("a").get('href')
                    links[h3]: str = link

            print(f"Processed page {page_count}!")
            # Increment page_count
            page_count += 1

        print(f"Finished {url}")

    # Return dict of whisky titles and links
    return links


def scrape_each_whisky(get_all_whiskys_data: Dict[str, str], headers: Dict[str, str]) -> Dict[str, str]:
    """Uses the get_all_whiskys() data to open links and scrape details on each whisky to build a dict.

    Args:
        get_all_whiskys_data (Dict[str, str]): result from get_all_whiskys()
        headers (Dict[str, str]): necessary Beautifulsoup4 headers

    Returns:
        dict: scraped whisky data for each whisky in get_all_whiskys_data and errors
    """

    # Initialise empty dicts for return
    scraped_data: Dict[str, str] = {}
    errors: Dict[str, str] = {}

    count: int = 1
    total: int = len(get_all_whiskys_data)

    # Begin loop over passed data
    for whisky in get_all_whiskys_data:
        if whisky in scraped_data:
            print(f"{whisky} already exists")
        else:
            try:
                print(f"[{count}/{total}] - Scraping {whisky} info...")
                req = requests.get(
                    f"{get_all_whiskys_data[whisky]}", headers)
                soup: BeautifulSoup = BeautifulSoup(req.content, 'html.parser')

                title: str = soup.find(
                    "h1", id='ContentPlaceHolder1_pageH1').get_text()

                initial_image = soup.find("div", id='imgProductBigDiv').find(
                    "div", class_='productImageWrap').find("img").get("src")

                image: str = "".join(initial_image[2:])

                # Attempt to get Varietal (Country)
                varietal: str = detailed_data(soup, "Country")

                # Attempt to get Region
                region: str = detailed_data(soup, "Region")

                # Attempt to get Brand
                brand: str = detailed_data(soup, "Distillery")

                # Attempt to get Age
                age: str = detailed_data(soup, "YearsMatured")

                # Attempt to get Style
                style: str = detailed_data(soup, "Style")

                # Attempt to get Alcohol Percentage
                alcohol_percentage: str = detailed_data(soup, "Alcohol")

                scraped_data[title] = {
                    "Country": "",
                    "Image": image,
                    "Varietal": varietal,
                    "Region": region,
                    "Whisky Style": style,
                    "Brand Name": brand,
                    "Name": title,
                    "Age": age,
                    "Alcohol Volume (%)": alcohol_percentage,
                    "Price ($ per bottle)": "",
                    "Peated (Y/N)": "",
                    "Rating ( /10)": ""}

                # print(data)
                print(f"Scraped {whisky}!")
            except AttributeError:
                print(f"Error on: {whisky}")
                errors[whisky] = get_all_whiskys_data[whisky]
                continue

            count += 1

    return {"scraped_data": scraped_data, "errors": errors}


def detailed_data(soup: BeautifulSoup, url_end: str) -> str:
    """Helper function for scrape_each_whisky() to return either one of three possible values.

    Args:
        soup (BeautifulSoup): initialised BeautifulSoup instance
        url_end (str): the suffix of the url to identify element

    Returns:
        str: value of element or empty string
    """
    result: str = ""

    try:
        result = soup.find("div", id=f'ContentPlaceHolder1_ctl00_ctl00_wd{url_end}').find(
            "span", class_='kv-val').find("a").get_text()
    except AttributeError:
        # Attempt to get alternative id value
        try:
            result = soup.find("div", id=f'ContentPlaceHolder1_ctl00_ctl01_wd{url_end}').find(
                "span", class_='kv-val').find("a").get_text()
        except AttributeError:
            return result

    return result
