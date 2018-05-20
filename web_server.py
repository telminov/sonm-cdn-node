from aiohttp import web


class DownloadFromCMS(web.View):
    async def get(self):
        uuid = self.request.match_info['uuid']
        return web.Response(text='test: %s' % uuid)


class Server:

    @staticmethod
    def run():
        app = web.Application()
        app.router.add_get('/asset/{uuid}', DownloadFromCMS)
        web.run_app(app, port=8000)


if __name__ == '__main__':
    Server.run()
