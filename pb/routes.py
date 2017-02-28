from pb.views.object import ObjectView
from pb.views.objects import ObjectsView


def setup_routes(app):
    app.router.add_route('*', '/objects', ObjectsView)
    app.router.add_route('*', '/object/{name}', ObjectView)
