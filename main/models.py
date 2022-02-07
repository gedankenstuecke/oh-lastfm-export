from django.db import models
from openhumans.models import OpenHumansMember
# Create your models here.


class LastFmUser(models.Model):
    oh_member = models.OneToOneField(
                    OpenHumansMember,
                    on_delete=models.CASCADE)
    username = models.CharField(max_length=256, default='')
