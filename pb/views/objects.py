from aiohttp import web

from pb.response import JSONResponse


class ObjectsView(web.View):
    async def post(self):
        objects = []
        storage = self.request.app['storage']
        reader = await self.request.multipart()

        while True:
            body_part = await reader.next()
            if not body_part:
                break

            obj = await storage.create_object(body_part.read_chunk)
            #obj.mimetype, _ = guess_type(body_part.filename)
            objects.append(obj.asdict())

        return JSONResponse(objects)
