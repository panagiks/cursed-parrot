from cursed.parrot.auth import login, logout


def make_routes(app):
    return [
        app.router.add_route('POST', r'/auth/', login),
        app.router.add_route('DELETE', r'/auth/', logout)
    ]
