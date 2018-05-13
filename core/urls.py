from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'assets/(?P<uuid>\w+)/&', views.download_from_master),
]
