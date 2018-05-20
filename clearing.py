"""
Чистака удаленных из CMS файлов
"""
from typing import Optional
import datetime
import aiohttp
import asyncio
import os

URL = 'http://cms.cdn.sonm.soft-way.biz/rest/assets/?dd__gte=%s'
LAST_CHECK_TIME_PATH = '/tmp/last_check_time.txt'


async def check_deleted(last_check_time: datetime.datetime):
    url = URL % last_check_time.isoformat(sep=' ')

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            deleted_assets = await response.json()

    for item in deleted_assets:
        asset_path = '/data/asset/%s' % item['uuid']
        os.unlink(asset_path)


async def periodical_checking():
    last_check_time = get_last_check_time() or datetime.datetime.now()

    while True:
        print('checking...')
        await check_deleted(last_check_time)

        save_last_check_time(last_check_time)
        last_check_time = datetime.datetime.now()

        print('sleeping...')
        await asyncio.sleep(60*5)


def get_last_check_time() -> Optional[datetime.datetime]:
    """Время последней проверки"""
    # из файла
    if os.path.isfile(LAST_CHECK_TIME_PATH):
        with open(LAST_CHECK_TIME_PATH, 'r') as f:
            last_check_time_iso = f.read()[:19]
            last_check_time = datetime.datetime.strptime(last_check_time_iso, '%Y-%m-%d %H:%M:%S')
            return last_check_time


def save_last_check_time(last_check_time:datetime.datetime):
    """запись времени последней проверки"""
    with open(LAST_CHECK_TIME_PATH, 'w') as f:
        f.write(last_check_time.isoformat(sep=' '))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodical_checking())
    loop.run_forever()
    loop.close()
