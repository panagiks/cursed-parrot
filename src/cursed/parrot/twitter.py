import uuid

from aiohttp import web
from aiohttp_session import get_session
from twython import Twython

from cursed.parrot import db


async def twitter_authorize(request):
    app = request.app
    auth = app['twitter'].get_authentication_tokens(
        callback_url=app['settings']['twitter']['callback_url']
    )
    await db.create_user(
        app,
        {
            'uuid': uuid.uuid4().hex,
            'oauth_token': auth['oauth_token'],
            'oauth_token_secret': auth['oauth_token_secret']
        }
    )
    return web.HTTPFound(
        location=auth['auth_url']
    )


async def twitter_callback(request):
    app = request.app
    oauth_token = request.query['oauth_token']
    oauth_verifier = request.query['oauth_verifier']
    user = await db.get_user_by_token(app, oauth_token)
    twitter = Twython(
        **app['settings']['twitter']['tokens'],
        oauth_token=oauth_token, oauth_token_secret=user.oauth_token_secret
    )
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    twitter = Twython(
        **app['settings']['twitter']['tokens'],
        oauth_token=final_step['oauth_token'],
        oauth_token_secret=final_step['oauth_token_secret']
    )
    profile = twitter.verify_credentials()
    user = await db.get_user(app, profile['screen_name'])
    if not user:
        user = await db.update_user(
            app,
            oauth_token,
            {
                'oauth_token': final_step['oauth_token'],
                'oauth_token_secret': final_step['oauth_token_secret'],
                'fullname': profile['name'],
                'username': profile['screen_name']
            }
        )
    session = await get_session(request)
    session['username'] = profile['screen_name']
    return web.HTTPFound(
        location=app.router['home'].url_for()
    )


async def twitter_update(request):
    app = request.app
    status = request.query['status']
    username = request.query['username']
    user = await db.get_user(app, username)
    if user:
        twitter = Twython(
            **app['settings']['twitter']['tokens'],
            oauth_token=user.oauth_token,
            oauth_token_secret=user.oauth_token_secret
        )
        twitter.update_status(status=status)
    return web.Response(text='Stay!')
