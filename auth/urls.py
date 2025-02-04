from django.urls import path
from . import views
from . import views_42

urlpatterns = [
    path('login/42/', views_42.login_redirect_42, name='login_redirect_42'),
    path('callback/42/', views_42.callback_42, name='callback_42'),
    path('logout/', views.logout, name='logout'),
]
