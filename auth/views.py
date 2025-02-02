import json
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from user.models import CustomUser

def test_view(request):
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
    redirect_uri = f'https://api.intra.42.fr/oauth/authorize?client_id={settings.OAUTH_UID_42}&redirect_uri={settings.OAUTH_REDIRECT_42}&response_type=code&response_type=code'
    return redirect(redirect_uri)

def callback_42(request):
    code = request.GET.get('code')

    # Obtain user's access code from 42 api
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

    access_token = response.json()['access_token']

    profile = get_profile_42(access_token)
    # print(profile['avatar'])

    user, _ = CustomUser.objects.get_or_create(oauth_id_42=profile['id'])
    user.username = profile['username']

    user.save()

    return redirect('/')

def get_profile_42(access_token):
    def get_image_file(image_url):
        response = requests.get(image_url)
        if response.status_code != 200:
            return None
        return response.content

    response = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code != 200:
        return None
    return {
        'id': response.json()['id'],
        'username': response.json()['login'],
        'avatar': get_image_file(response.json()['image']['link']),
    }