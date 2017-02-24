from mimetypes import guess_type

from aiohttp import web

from pb.storage import filesystem


storage_impl = filesystem


class PastesView(web.View):
    async def post(self):
        reader = await self.request.multipart()

        while True:
            body_part = await reader.next()
            if not body_part:
                break

            paste = await storage_impl.write_body(body_part)
            paste.generate_label(
                label=self.request.match_info.get('name'))
            paste.mimetype, _ = guess_type(body_part.filename)

            await storage_impl.write_metadata(paste)

            print(paste)

        return web.Response(text='thx')
