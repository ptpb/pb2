from aiohttp import web


from pb.storage import filesystem


storage_impl = filesystem


class PasteView(web.View):
    async def get(self):

        stream = web.StreamResponse()
        await stream.prepare(self.request)

        await storage_impl.stub(
            self.request.match_info['name'], stream)

        return stream
