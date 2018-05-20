from aiohttp import web
import aiohttp
import aiofiles
import psutil


class DownloadFromCMS(web.View):
    """
    Прокси. Запрашивает файл из CMS и сохранет его для nginx локально.
    """
    url = 'http://cms.cdn.sonm.soft-way.biz/asset/%s/'

    async def get(self):
        uuid = self.request.match_info['uuid']
        url = self.url % uuid

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                asset_data = await response.read()

        if response.status == 200:
            async with aiofiles.open('/data/asset/%s' % uuid, 'wb') as f:
                await f.write(asset_data)

        return web.Response(body=asset_data, headers=response.headers)


class BytesSent(web.View):
    """
    Объем отправленного трафика
    """

    async def get(self):
        bytes_sent = psutil.net_io_counters().bytes_sent
        return web.Response(text=str(bytes_sent))


class Server:

    @staticmethod
    def run():
        app = web.Application()
        app.router.add_get('/asset/{uuid}', DownloadFromCMS)
        app.router.add_get('/bytes_sent', BytesSent)
        web.run_app(app, port=8000)


if __name__ == '__main__':
    Server.run()
