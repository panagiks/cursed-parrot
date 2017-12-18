import uuid

from aiohttp import web
from aiohttp_session import get_session
from aiohttp.web_response import json_response
from passlib.hash import sha512_crypt
# sha512_crypt.hash(password)


async def user_create(request):
    # TODO: Make sure user doesn't already exist
    try:
        username = payload['username']
        password = payload['password']
        email = payload['email']
    except KeyError:
        pass
    async with request.app['pool'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM users WHERE username = %s;",
                (username)
            )
            res = await cursor.fetchone()
    if len(res):
        raise web.HTTPBadRequest()
    if 'is_hash' not in payload or not payload['is_hash']:
        password = sha512_crypt.hash(password)
