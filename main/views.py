from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
import json
from openhumans.models import OpenHumansMember
from .models import LastFmUser


def index(request):
    """
    Starting page for app.
    """
    try:
        auth_url = OpenHumansMember.get_auth_url()
    except ImproperlyConfigured:
        auth_url = None
    if not auth_url:
        messages.info(request,
                      mark_safe(
                          '<b>You need to set up your ".env"'
                          ' file!</b>'))

    context = {'auth_url': auth_url}
    if request.user.is_authenticated:
        if hasattr(request.user.openhumansmember, 'lastfmuser'):
            context['lastfmuser'] = request.user.openhumansmember.lastfmuser.username
    return render(request, 'main/index.html', context=context)


def about(request):
    """
    give FAQ and further details on the app
    """
    return render(request, 'main/about.html')


def logout_user(request):
    """
    Logout user
    """
    if request.method == 'POST':
        logout(request)
    redirect_url = settings.LOGOUT_REDIRECT_URL
    return redirect(redirect_url)


def create_lastfm(request):
    """
    collect fitbit client id/Secret
    """
    if request.method == 'POST':
        if hasattr(request.user.openhumansmember, 'lastfmuser'):
            lastfm_user = request.user.openhumansmember.lastfmuser
        else:
            lastfm_user = LastFmUser()
        lastfm_user.oh_member = request.user.openhumansmember
        lastfm_user.username = request.POST.get('username')
        lastfm_user.save()
    return redirect('/')


def delete_lastfm(request):
    if request.method == 'POST':
        if hasattr(request.user.openhumansmember, 'lastfmuser'):
            lastfm_user = request.user.openhumansmember.lastfmuser
            lastfm_user.delete()
    return redirect('/')


@csrf_exempt
def deauth_hook(request):
    if request.method == 'POST':
        print(request.body)
        print(request.META)
        print(json.loads(request.body))
        print(request.POST.get('project_member_id'))
        print(request.POST.get('erasure_requested'))
    return redirect('/')
