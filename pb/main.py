import asyncio
import logging
import sys

from aiohttp import web

from pb.routes import setup_routes


def init(loop, argv):
    app = web.Application(loop=loop)

    setup_routes(app)

    return app


def main(argv):
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    app = init(loop, argv)
    web.run_app(app)


if __name__ == '__main__':
    main(sys.argv[1:])
