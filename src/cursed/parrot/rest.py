import asyncio
import aiohttp_jinja2
import base64
import jinja2

from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
from twython import Twython

from cursed.parrot.route import make_routes
from cursed.parrot.db import init_pg, close_pg, get_oauth_provider


async def get_app():
    app = web.Application()
    app['settings'] = {
        'twitter': {
            'callback_url': 'https://localhost:port/twitter/'
        },
        'db': {
            'database': 'postgres',
            'user': 'postgres',
            'password': '123',
            'host': '127.0.0.1',
            'port': '5432'
        }
    }  # Get settings
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader('src/cursed/parrot/templates')
    )
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app.on_startup.append(init_pg)
    app.on_startup.append(get_twitter_keys)
    app.on_cleanup.append(close_pg)
    make_routes(app)
    return app


async def get_twitter_keys(app):
    provider = await get_oauth_provider(app, 'twitter')
    app['settings']['twitter']['tokens'] = {
        'app_key': provider.app_key,
        'app_secret': provider.app_secret
    }
    app['twitter'] = Twython(**app['settings']['twitter']['tokens'])


def aio_rest():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app())
    web.run_app(app, port=8080, host='127.0.0.1')


if __name__ == '__main__':
    aio_rest()
else:
    APP = asyncio.get_event_loop().run_until_complete(get_app())
