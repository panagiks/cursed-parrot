import asyncio

from aiohttp import web

from cursed.parrot.route import make_routes


async def get_app():
    app = web.Application()
    app['pool'] = await aiomysql.create_pool()  # Add settings
    make_routes(app)
    return app


def aio_rest():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app())
    web.run_app(app, port=8080, host='127.0.0.1')


if __name__ == '__main__':
    aio_rest()
else:
    APP = asyncio.get_event_loop().run_until_complete(get_app())
