import json

with open('whiskeys_new_output.json', 'r') as file_read:
    parsed_data = json.load(file_read)

print(len(parsed_data))
