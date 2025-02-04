from django.urls import path
from . import views
from . import views_42
from . import views_github

urlpatterns = [
    path('login/42/', views_42.login_redirect_42, name='login_redirect_42'),
    path('callback/42/', views_42.callback_42, name='callback_42'),

    path('login/github/', views_github.login_redirect_github, name='login_redirect_github'),
    path('callback/github/', views_github.callback_github, name='callback_github'),

    path('logout/', views.logout, name='logout'),
]
