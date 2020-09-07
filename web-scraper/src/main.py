import json
import time
from typing import Dict, List
from scraping_functions import get_all_whiskys, scrape_each_whisky, detailed_data


def main():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    # urls: List[str] = ["https://www.masterofmalt.com/age/10-year-old-whisky",
    #                    "https://www.masterofmalt.com/age/12-year-old-whisky", "https://www.masterofmalt.com/age/18-year-old-whisky", "https://www.masterofmalt.com/age/21-year-old-whisky"]

    # NOTE Use this if there is no whiskys_output.json file
    # whisky_links: Dict[str, str] = get_all_whiskys(urls, headers)

    # NOTE Use this if already written result of GetAllwhiskys() to the whiskys_output.json file
    with open('whiskeys_output.json', 'r') as whisky_output:
        whisky_links: dict = json.load(whisky_output)

    whisky_output: Dict[str, str] = scrape_each_whisky(whisky_links, headers)

    with open("whisky_final_output.json", "w") as whisky_final_output:
        json.dump(whisky_output["scraped_data"], whisky_final_output)

    with open("errors.json", "w") as whisky_scrape_errors:
        json.dump(whisky_output["errors"], whisky_scrape_errors)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Time taken: {end - start}s")
