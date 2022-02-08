from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember
from main import helpers
from main.models import LastFmUser
from main.tasks import last_fm_data
import requests


class Command(BaseCommand):
    help = 'Process so far unprocessed data sets'

    def handle(self, *args, **options):
        requests.get('https://oh-lastfm-export.herokuapp.com/')
        #how to keep the heroku app alive despite a free dyno :joy:
        lastfm_users = LastFmUser.objects.all()
        for l in lastfm_users:
            last_fm_data.delay(l.oh_member.oh_id)
