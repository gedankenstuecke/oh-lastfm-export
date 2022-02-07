import json
import requests


def get_existing_file(oh_member):
    files = oh_member.list_files()
    for f in files:
        if f['basename'] == 'lastfm-data.json':
            data = json.loads(requests.get(f['download_url']).content)
            return data
    return []


def get_timestamp(data):
    for entry in data:
        if 'date' in entry.keys():
            return entry['date']['uts']
