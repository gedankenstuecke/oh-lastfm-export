from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/?$', views.logout_user, name='logout'),
    url(r'^about/?$', views.about, name='about'),
    url(r'^create-lastfm/?$', views.create_lastfm, name='create-lastfm'),
    url(r'^delete-lastfm/?$', views.delete_lastfm, name='delete-lastfm'),
    url(r'^deauth_hook/?$', views.deauth_hook, name='deauth_hook'),
]
