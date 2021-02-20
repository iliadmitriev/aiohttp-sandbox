from views.render import RenderView
from views.index import IndexView
from views.ping import PingView
from views.jinja import JinjaView


def setup_routes(app):
    app.router.add_view('/jinja', JinjaView)
    app.router.add_view('/ping', PingView)
    app.router.add_view('/', IndexView)
    app.router.add_view('/render', RenderView)
