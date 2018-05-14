from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'asset/(?P<uuid>\w+)/$', views.download_from_master),
]
