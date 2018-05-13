import os
import requests

from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView


class DownloadFromMaster(APIView):
    def get(self, *args, **kwargs):
        file_data = self.get_file()
        status = 404

        if file_data:
            status = 200
            self.save_file(file_data)

        return HttpResponse(file_data, status=status)

    def get_file(self):
        url = self.get_file_url()
        file_data = b''

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                response.raw.decode_content = True
                file_data = response.raw.read()

        except requests.ConnectionError:
            pass

        return file_data

    def save_file(self, file_data: bytes):
        with open(self.get_file_path(), 'wb') as fl:
            fl.write(file_data)


    def get_file_url(self) -> str:
        uuid = self.kwargs.get('uuid')
        master_url = self.get_master_url()
        url = os.path.join(master_url, 'assets', uuid)

        return url

    def get_file_path(self) -> str:
        uuid = self.kwargs.get('uuid')
        data_path = self.get_data_path()
        file_path = os.path.join(data_path, uuid)

        return file_path

    @staticmethod
    def get_master_url() -> str:
        return settings.MASTER_URL.strip('/')

    @staticmethod
    def get_data_path() -> str:
        return settings.DATA_DIR.strip('/')

download_from_master = DownloadFromMaster.as_view()
