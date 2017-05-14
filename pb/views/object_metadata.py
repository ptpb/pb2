from aiohttp import web
from aiohttp.web_response import json_response

from pb.models.object import ObjectSchema


schema = ObjectSchema()


class ObjectMetadataView(web.View):
    async def get(self):
        storage = self.request.app['storage']

        obj = await storage.read_metadata(
            self.request.match_info['id'])

        result = schema.dump(obj)
        return json_response(result.data)

    async def patch(self):
        storage = self.request.app['storage']

        obj = await storage.read_metadata(
            self.request.match_info['id'])

        content = await self.request.json()
        obj.update(**schema.load(content).data)

        await storage.write_metadata(obj)

        result = schema.dump(obj)
        return json_response(result.data)
