from functools import partial

from aiohttp import web
from aiohttp.web_response import json_response

from pb.models.object import ObjectSchema


schema = ObjectSchema()


class ObjectsView(web.View):
    async def post(self):
        storage = self.request.app['storage']

        read_chunk = partial(self.request.content.read, 8192)
        obj = await storage.create_object(read_chunk)

        result = schema.dump(obj)

        return json_response(result.data)
