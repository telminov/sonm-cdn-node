from django.urls import path

from core import views

urlpatterns = [
    path('asset/<uuid>', views.DownloadFromCMS.as_view(), name='download_from_cms'),
]
