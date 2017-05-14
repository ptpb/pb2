from pb.views.object import ObjectView
from pb.views.object_metadata import ObjectMetadataView
from pb.views.objects import ObjectsView


def setup_routes(app):
    app.router.add_route('*', '/objects', ObjectsView)
    app.router.add_route('*', '/objects/{id}', ObjectView)
    app.router.add_route('*', '/objects/{id}/metadata', ObjectMetadataView)
