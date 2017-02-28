from aiohttp import web


class ObjectView(web.View):
    async def get(self):
        storage = self.request.app['storage']
        stream = web.StreamResponse()
        await stream.prepare(self.request)

        await storage.read_object(
            self.request.match_info['name'], stream.write)

        return stream
