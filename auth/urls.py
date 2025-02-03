from django.urls import path
from . import views
from . import views_github

urlpatterns = [
    path('test/', views.test_view, name='test_view'),

    path('login/42/', views.login_redirect_42, name='login_redirect_42'),
    path('callback/42/', views.callback_42, name='callback_42'),
    path('logout/', views.logout, name='logout'),

    path('login/github/', views_github.login_redirect_github, name='login_redirect_github'),
]
