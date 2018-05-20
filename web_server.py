from aiohttp import web
import aiohttp
import aiofiles


class DownloadFromCMS(web.View):
    url = 'http://cms.cdn.sonm.soft-way.biz/asset/%s/'

    async def get(self):
        uuid = self.request.match_info['uuid']
        url = self.url % uuid

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                asset_data = await response.read()

        async with aiofiles.open('/data/asset/%s' % uuid, 'wb') as f:
            await f.write(asset_data)

        return web.Response(body=asset_data, headers=response.headers)


class Server:

    @staticmethod
    def run():
        app = web.Application()
        app.router.add_get('/asset/{uuid}', DownloadFromCMS)
        web.run_app(app, port=8000)


if __name__ == '__main__':
    Server.run()
