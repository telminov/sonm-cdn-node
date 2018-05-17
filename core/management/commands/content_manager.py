import time

import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core import models


class Command(BaseCommand):
    DEFAULT_SLEEP_TIME = 60 * 5

    def add_arguments(self, parser):
        parser.add_argument(
            '--infinitely',
            dest='infinitely',
            action='store_true',
            help=u'Бесконечный цикл, смотрим на изменения и удаляем что надо',
        )
        parser.add_argument(
            '--time',
            dest='time',
            type=int,
            help=u'С какой периодичностью запускать проверку (в секундах)',
        )

    def handle(self, *args, **options):
        self.sleep_time = options.get('time') or self.DEFAULT_SLEEP_TIME

        if options.get('infinitely'):
            while True:
                self.manage()
                time.sleep(self.sleep_time)
        else:
            self.manage()

    def manage(self):
        deleted_assets = self.get_deleted_assets()
        data_path = self.get_data_path()
        for asset in deleted_assets:
            try:
                os.remove(os.path.join(data_path, asset['uuid']))
            except OSError:
                pass

        models.CMSLog.objects.create(
            action=models.CMSLog.ACTION_CHOICES[0][0],
            message='Удаленные файлы синхронизированы'
        )


    def get_deleted_assets(self):
        response = requests.get(self.get_deleted_assets_url(), self.get_deleted_assets_params())
        assets = response.json()

        return assets

    def get_deleted_assets_url(self):
        return os.path.join(self.get_cms_url(), 'rest', 'assets')

    def get_deleted_assets_params(self):
        last_checked = self.get_last_checked_datetime()
        params = {}
        if last_checked:
            params['dd__gte'] = last_checked.isoformat()

        return params

    @staticmethod
    def get_last_checked_datetime():
        last_log = models.CMSLog.objects.filter(action=models.CMSLog.ACTION_CHOICES[0][0]).last()
        last_checked = None

        if last_log:
            last_checked = last_log.dc

        return last_checked

    @staticmethod
    def get_cms_url() -> str:
        return settings.CMS_URL.strip('/')

    @staticmethod
    def get_data_path() -> str:
        return settings.DATA_DIR.rstrip('/')