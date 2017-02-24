from pb.views.paste import PasteView
from pb.views.pastes import PastesView


def setup_routes(app):
    app.router.add_route('*', '/pastes', PastesView)
    app.router.add_route('*', '/pastes/{name}', PastesView)
    app.router.add_route('*', '/paste/{name}', PasteView)
