import time

from aiohttp import web
from aiohttp_session import get_session
from aiohttp.web_response import json_response
from passlib.hash import sha512_crypt
# sha512_crypt.hash(password)
# sha512_crypt.verify(password, hash)


async def login(request):
    try:
        username = payload['username']
        password = payload['password']
    except KeyError:
        raise web.HTTPBadRequest()
    async with request.app['pool'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT password_hash FROM users WHERE username = %s;",
                (username)
            )
            res = await cursor.fetchone()
    # TODO: Check if res has any data and check against password_hash
    try:
        (res,) = res
    except ValueError:
        raise web.HTTPBadRequest()
    # sha512_crypt.verify(password, hash)
    if 'is_hash' in payload and payload['is_hash']:
        valid = (res == password)
    else:
        valid = sha512_crypt.verify(password, res)
    if not valid:
        raise web.HTTPBadRequest()
    session = await get_session(request)
    session['last_visit'] = time.time()
    session['user'] = username
    return web.Response(status=204)


async def logout(request):
    session = await get_session(request)
    if not session.new:
        session.invalidate()
    return web.Response(status=204)
