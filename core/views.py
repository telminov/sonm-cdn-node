import os
import requests

from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework.views import APIView


class DownloadFromCMS(APIView):
    def get(self, *args, **kwargs):
        cms_response  = self.get_cms_response()

        if cms_response.status_code == 200:
            self.save_file(cms_response.content)
            
        return cms_response  

    def get_cms_response(self):
        try:
            rq_response = requests.get(self.get_download_file_url(), stream=True)
            rq_response.raw.decode_content = True
            django_response = HttpResponse(
                content=rq_response.content,
                status=rq_response.status_code
            )

            for key, value in rq_response.headers.items():
                if key != 'Content-Disposition':
                    django_response[key] = value

        except requests.ConnectionError:
            django_response = HttpResponse(
                "{uuid} does not exist.".format(uuid=self.get_file_uuid()),
                status=404
            )

        return django_response

    def save_file(self, file_data: bytes):
        with open(self.get_file_path(), 'wb') as fl:
            fl.write(file_data)

    def get_file_path(self) -> str:
        uuid = self.kwargs.get('uuid')
        data_path = self.get_data_path()
        file_path = os.path.join(data_path, uuid)

        return file_path

    def get_file_uuid(self):
        return self.kwargs['uuid']

    def get_download_file_url(self):
        cms_url = self.get_cms_url()
        uuid = self.get_file_uuid()
        download_url = os.path.join(cms_url, 'asset', uuid)

        return download_url

    @staticmethod
    def get_cms_url() -> str:
        return settings.CMS_URL.strip('/')

    @staticmethod
    def get_data_path() -> str:
        return settings.DATA_DIR.rstrip('/')

download_from_cms = DownloadFromCMS.as_view()
