import shutil
import requests
import pathlib


from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView


class DownloadFromMaster(APIView):
    def get(self, *args, **kwargs):
        path = kwargs.get('path')
        data = b''
        status = 404

        try:
            response = requests.get(settings.MASTER_URL + '/' + path, stream=True)
            if response.status_code == 200:
                file_path = settings.DATA_DIR + path
                dr = path.split('/')[:-1]
                print(dr)
                if dr:
                    dr = settings.DATA_DIR + '/'.join(dr)
                    pathlib.Path(dr).mkdir(parents=True, exist_ok=True)

                with open(file_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                    status = 200

                # TODO
                with open(file_path, 'rb') as f:
                    data = f.read()

        except requests.ConnectionError:
            pass


        return HttpResponse(data, status=status, content_type='image/png') # TODO

download_from_master = DownloadFromMaster.as_view()
