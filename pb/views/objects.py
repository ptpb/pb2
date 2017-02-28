from aiohttp import web


class ObjectsView(web.View):
    async def post(self):
        storage = self.request.app['storage']
        reader = await self.request.multipart()

        while True:
            body_part = await reader.next()
            if not body_part:
                break

            paste = await storage.create_object(body_part.read_chunk)
            #paste.mimetype, _ = guess_type(body_part.filename)

            print(paste)

        return web.Response(text='thx')
