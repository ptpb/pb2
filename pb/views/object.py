from aiohttp import web


class ObjectView(web.View):
    async def get(self):
        storage = self.request.app['storage']

        response = web.StreamResponse()
        await response.prepare(self.request)

        # fixme: metadata should read before prepare()
        await storage.read_object(
            self.request.match_info['id'], response.write)

        return response
