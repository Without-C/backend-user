from django.shortcuts import redirect

def logout(request):
    response = redirect('/')
    response.delete_cookie('jwt')
    response.delete_cookie('jwt_refresh')
    response.delete_cookie('username')
    response.delete_cookie('avatar_url')
    return response