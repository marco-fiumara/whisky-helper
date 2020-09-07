import csv
import json


def read_csv(path: str) -> dict:
    parsed_data: dict = {}
    reader = csv.DictReader(open(path))
    for row in reader:
        parsed_data[row['Name']] = row

    return parsed_data


parsed_whisky_data = read_csv('Friskey Whiskey - Sheet1.csv')

# search = input("Region: ")

regions: dict = {}

for whisky in parsed_whisky_data:
    region = parsed_whisky_data[whisky]['Region']
    if region not in regions:
        regions[region] = 0
    else:
        regions[region] += 1

print(regions)

with open('parsed_data.json', 'w') as json_data:
    json.dump(parsed_whisky_data, json_data)
