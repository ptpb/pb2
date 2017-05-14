from aiohttp import web


class ObjectView(web.View):
    async def get(self):
        storage = self.request.app['storage']

        response = web.StreamResponse()

        obj = await storage.read_metadata(
            self.request.match_info['id'])

        response.headers['content-type'] = obj.mimetype

        await response.prepare(self.request)

        await storage._read_body(
            self.request.match_info['id'], response.write)

        return response
