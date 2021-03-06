import json
import time
import datetime
import tempfile
import requests
from openhumans.models import OpenHumansMember
from celery import shared_task
import os
from .helpers import get_existing_file_latest, get_timestamp
from .helpers import get_existing_year_file
import datetime

LASTFM_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&api_key={}&format=json&limit=50".format(
    os.getenv('LASTFM_KEY')
)


@shared_task
def last_fm_data(oh_member_id):
    oh_member = OpenHumansMember.objects.get(oh_id=oh_member_id)
    lastfm_user = oh_member.lastfmuser.username
    print('trying to update {}/{}'.format(lastfm_user, oh_member_id))
    user_url = LASTFM_URL + "&user={}".format(lastfm_user)
    old_data = get_existing_file_latest(oh_member)
    if old_data:
        from_timestamp = get_timestamp(old_data)
        user_url = user_url + "&from={}".format(from_timestamp)
        print('got old data')
        print(user_url)
    else:
        to_timestamp = int(datetime.datetime.utcnow().timestamp())
        user_url = user_url + "&to={}".format(to_timestamp)
        print('no old data')
        print(user_url)
    first_request = requests.get(user_url).json()
    print(first_request.keys())
    tracks = first_request['recenttracks']['track']
    pages = first_request['recenttracks']['@attr']['totalPages']
    # for i in range(2, 50):
    for i in range(2, int(pages)):
        print(i)
        time.sleep(1)
        p_url = user_url + "&page={}".format(i)
        page = requests.get(p_url).json()
        tracks = tracks + page['recenttracks']['track']
    per_year = {}
    for song in tracks:
        if 'date' in song.keys():
            year = datetime.datetime.fromtimestamp(int(song['date']['uts'])).year
            if str(year) in per_year.keys():
                per_year[str(year)].append(song)
            else:
                per_year[str(year)] = [song]
    for year, songs in per_year.items():
        old_data = get_existing_year_file(oh_member, year)
        songs = songs + old_data
        with tempfile.TemporaryFile() as f:
            js = json.dumps(songs)
            js = str.encode(js)
            f.write(js)
            f.flush()
            f.seek(0)
            oh_member.delete_single_file(
                file_basename='lastfm-data-{}.json'.format(year))
            oh_member.upload(
                f, "lastfm-data-{}.json".format(year), metadata={
                    "description": "last.fm scrobbling history",
                    "tags": ["lastfm", 'scrobbles', 'music']
                    })
            print('updated data for {}/{}'.format(lastfm_user, year))
