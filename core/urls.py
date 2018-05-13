from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'(?P<path>.*)', views.download_from_master),
]
