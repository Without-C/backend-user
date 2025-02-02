import os
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
]

urlpatterns += static('/avatars/', document_root=os.path.join(settings.BASE_DIR, 'avatars'))
