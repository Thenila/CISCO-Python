import json
import os

def read_from_file(filename='flights.json'):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []
    with open(filename, 'r') as file:
        return json.load(file)

def write_to_file(data, filename='flights.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)