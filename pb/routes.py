from pb.views.paste import PasteView
from pb.views.pastes import PastesView


def setup_routes(app):
    app.router.add_route('*', '/objects', ObjectsView)
    app.router.add_route('*', '/object/{name}', ObjectView)
