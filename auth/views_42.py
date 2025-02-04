import os
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.base import ContentFile
from user.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_image_file, get_random_filename

def login_redirect_42(request):
    """
    42 로그인 페이지로 redirect
    """
    redirect_uri = f'https://api.intra.42.fr/oauth/authorize?client_id={settings.OAUTH_UID_42}&redirect_uri={settings.OAUTH_REDIRECT_42}&response_type=code&response_type=code'
    return redirect(redirect_uri)

def callback_42(request):
    code = request.GET.get('code')

    # 42 서버로부터 access token 가져오기
    response = requests.post("https://api.intra.42.fr/oauth/token", data={
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH_UID_42,
        'client_secret': settings.OAUTH_SECRET_42,
        'code': code,
        'redirect_uri': settings.OAUTH_REDIRECT_42,
    })
    if response.status_code != 200:
        # 42 서버로부터 access code 받아오는 것을 실패하면 어떻게 예외 처리하지?
        return redirect('/')

    # 가져온 access token으로 사용자 이름, 사진 가져오기
    access_token = response.json()['access_token']
    profile = get_profile_42(access_token)
    if profile == None:
        return redirect('/')

    # 새로운 유저라면 DB에 사용자 이름과 사진을 저장
    user, created = CustomUser.objects.get_or_create(oauth_id_42=profile['id'])
    if created:
        user.username = profile['username']
        if profile['avatar_content'] != None:
            user.avatar.save(profile['avatar_filename'], ContentFile(profile['avatar_content']))
        user.save()

    # JWT 생성
    refresh_token_obj = RefreshToken.for_user(user)
    access_token_str = str(refresh_token_obj.access_token)
    refresh_token_str = str(refresh_token_obj)

    # response 생성
    response = redirect('/')
    response.set_cookie('jwt', access_token_str, httponly=True, secure=True)
    response.set_cookie('jwt_refresh', refresh_token_str, httponly=True, secure=True)
    response.set_cookie('username', user.username)
    response.set_cookie('avatar_url', os.path.basename(user.avatar.name) if user.avatar else '')
    return response

def get_profile_42(access_token):
    # access token을 이용하여 42 서버에 사용자 정보 요청
    response = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code != 200:
        return None

    # 얻은 사용자 정보 중 intra id와 profile 사진을 추출
    image_url = response.json()['image']['versions']['small']
    return {
        'id': response.json()['id'],
        'username': response.json()['login'],
        'avatar_content': get_image_file(image_url),
        'avatar_filename': get_random_filename(image_url)
    }