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

def test_view(request):
    """
    테스트용 view
    """
    if request.method == 'GET':
        return JsonResponse({
            'message': 'get test',
            'status': 'success'
        })

    elif request.method == 'POST':
        try:
            received_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        return JsonResponse({
            'message': 'post test',
            'data_received': received_data,
            'status': 'success'
        })

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

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
    access_token_obj = refresh_token_obj.access_token
    access_token_obj['username'] = user.username
    access_token_obj['avatar_url'] = user.avatar.url if user.avatar else ''
    access_token_str = str(access_token_obj)
    refresh_token_str = str(refresh_token_obj)

    # response 생성
    response = redirect('/')
    response.set_cookie('jwt', access_token_str, httponly=True, secure=True)
    response.set_cookie('jwt_refresh', refresh_token_str, httponly=True, secure=True)
    return response

def get_profile_42(access_token):
    def get_image_file(image_url):
        """
        주어진 image_url으로부터 사진 다운로드
        """
        response = requests.get(image_url)
        if response.status_code != 200:
            return None
        return response.content

    def get_random_filename(image_url):
        """
        주어진 image_url으로부터 얻은 이미지 확장자를 유지하며, 무작위 파일 이름 생성
        """
        original_filename = os.path.basename(urlparse(image_url).path)
        _, ext = os.path.splitext(original_filename)
        random_filename = uuid.uuid4().hex
        return f"{random_filename}{ext}"

    # access token을 이용하여 42 서버에 사용자 정보 요청
    response = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code != 200:
        return None

    # 얻은 사용자 정보 중 intra id와 profile 사진을 추출
    image_url = response.json()['image']['link']
    return {
        'id': response.json()['id'],
        'username': response.json()['login'],
        'avatar_content': get_image_file(image_url),
        'avatar_filename': get_random_filename(image_url)
    }

def logout(request):
    response = redirect('/')
    response.delete_cookie('jwt')
    response.delete_cookie('jwt_refresh')
    return response