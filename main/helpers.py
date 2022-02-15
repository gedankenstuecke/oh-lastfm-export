import json
import requests


def get_existing_file_latest(oh_member):
    files = oh_member.list_files()
    lastfm_files = []
    for f in files:
        if f['basename'].startswith('lastfm-data'):
            lastfm_files.append(f['basename'])
    if len(lastfm_files) > 0:
        target_file = sorted(lastfm_files)[-1]
        for f in files:
            if f['basename'] == target_file:
                data = json.loads(requests.get(f['download_url']).content)
                return data
    return []


def get_timestamp(data):
    for entry in data:
        if 'date' in entry.keys():
            return entry['date']['uts']


def get_existing_year_file(oh_member, year):
    files = oh_member.list_files()
    for f in files:
        if f['basename'] == ('lastfm-data-{}.json'.format(year)):
            data = json.loads(requests.get(f['download_url']).content)
            return data
    return []
