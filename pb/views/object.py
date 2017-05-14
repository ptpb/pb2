from aiohttp import web


class ObjectView(web.View):
    async def get(self):
        storage = self.request.app['storage']

        response = web.StreamResponse()

        obj = await storage.read_metadata(
            self.request.match_info['id'])

        if obj.mimetype is not None:
            response.headers['content-type'] = obj.mimetype

        await response.prepare(self.request)

        await storage.read_object(
            self.request.match_info['id'], response.write)

        return response
