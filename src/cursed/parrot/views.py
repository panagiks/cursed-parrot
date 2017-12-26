import binascii
import uuid

from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from datetime import datetime
from oscrypto import asymmetric

from cursed.parrot import db


@template('home.html')
async def home(request):
    session = await get_session(request)
    ret = {'user': session['username']} if 'username' in session else {}
    return ret


async def create_message(request):
    body = await request.post()
    session = await get_session(request)
    message = bytes(body['message'], 'UTF-8')
    date = datetime.strptime(body['date'], '%Y-%m-%d')
    public_key, private_key = asymmetric.generate_pair('rsa', bit_size=4096)
    ciphertext = asymmetric.rsa_oaep_encrypt(public_key, message)
    private_key = asymmetric.dump_private_key(private_key, None)
    user = await db.get_user(request.app, session['username'])
    message_uuid = uuid.uuid4().hex
    await db.create_message(
        request.app,
        {
            'uuid': message_uuid,
            'user': user.uuid,
            'private_key': binascii.hexlify(private_key).decode('UTF-8'),
            'ciphertext': binascii.hexlify(ciphertext).decode('UTF-8'),
            'expires': date
        }
    )
    return web.HTTPFound(
        location=request.app.router['message_detail'].url_for(
            uuid=message_uuid
        )
    )


@template('messages.html')
async def messages_list(request):
    session = await get_session(request)
    user = await db.get_user(request.app, session['username'])
    messages = await db.list_messages(request.app, user.uuid)
    ret = {'user': session['username']} if 'username' in session else {}
    ret['messages'] = messages
    return ret


@template('message.html')
async def message_detail(request):
    session = await get_session(request)
    user = await db.get_user(request.app, session['username'])
    message = await db.get_message(
        request.app,
        request.match_info['uuid'],
        user.uuid
    )
    try:
        decrypt = request.query['decrypt']
    except KeyError:
        decrypt = False
    ret = {'user': session['username']} if 'username' in session else {}
    if decrypt:
        ret['text'] = asymmetric.rsa_oaep_decrypt(
            asymmetric.load_private_key(
                binascii.unhexlify(message.private_key.lstrip("\\x"))
            ),
            binascii.unhexlify(message.ciphertext.lstrip("\\x"))
        )
    ret['message'] = message
    return ret
