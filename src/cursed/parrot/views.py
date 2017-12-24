from aiohttp_jinja2 import template
from aiohttp_session import get_session
from oscrypto import asymmetric


@template('home.html')
async def home(request):
    session = await get_session(request)
    ret = {'user': session['username']} if 'username' in session else {}
    return ret


async def create_message(request):
    body = await request.post()
    message = bytes(body['message'], 'UTF-8')
    date = body['date']
    public_key, private_key = asymmetric.generate_pair('rsa', bit_size=4096)
    ciphertext = asymmetric.rsa_oaep_encrypt(public_key, message)
    print(private_key)
