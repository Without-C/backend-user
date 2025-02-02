from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test_view'),
    path('login/42/', views.login_redirect_42, name='login_redirect_42'),
]
