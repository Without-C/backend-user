import os
import json
import uuid
import requests
from urllib.parse import urlparse
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.core.files.base import ContentFile
from user.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

def login_redirect_github(request):
    """
    42 로그인 페이지로 redirect
    """
    redirect_uri = f'https://github.com/login/oauth/authorize?client_id={settings.OAUTH_UID_GITHUB}&redirect_uri={settings.OAUTH_REDIRECT_GITHUB}'
    return redirect(redirect_uri)