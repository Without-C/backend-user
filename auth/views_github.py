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

def callback_github(request):
    code = request.GET.get('code')

    # 42 서버로부터 access token 가져오기
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={
            'Accept': 'application/json',
        },
        data={
            'client_id': settings.OAUTH_UID_GITHUB,
            'client_secret': settings.OAUTH_SECRET_GITHUB,
            'code': code,
            'redirect_uri': settings.OAUTH_REDIRECT_GITHUB,
        }
    )
    if response.status_code != 200:
        # 42 서버로부터 access code 받아오는 것을 실패하면 어떻게 예외 처리하지?
        return redirect('/')

    # 가져온 access token으로 사용자 이름, 사진 가져오기
    access_token = response.json()['access_token']

    # response 생성
    response = redirect('/')
    return response
