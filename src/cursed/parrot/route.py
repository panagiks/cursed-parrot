from cursed.parrot.auth import login, logout
from cursed.parrot.twitter import twitter_authorize, twitter_callback, twitter_update
from cursed.parrot.views import home, create_message, messages_list, message_detail


def make_routes(app):
    return [
        app.router.add_route('GET', r'/', home, name='home'),
        # app.router.add_route('POST', r'/auth/', login),
        app.router.add_route('GET', r'/logout/', logout, name='logout'),
        app.router.add_route('GET', r'/twitter/auth/', twitter_authorize, name='tw_login'),
        app.router.add_route('GET', r'/twitter/', twitter_callback),
        app.router.add_route('GET', r'/twitter/status/', twitter_update),
        app.router.add_route('POST', r'/message/', create_message, name='create_message'),
        app.router.add_route('GET', r'/message/', messages_list, name='messages_list'),
        app.router.add_route('GET', r'/message/{uuid}/', message_detail, name='message_detail')
    ]
