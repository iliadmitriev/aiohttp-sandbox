from views.Render import RenderView
from views.Index import IndexView
from views.Ping import PingView
from views.Jinja import JinjaView


def setup_routes(app):
    app.router.add_view('/jinja', JinjaView)
    app.router.add_view('/ping', PingView)
    app.router.add_view('/', IndexView)
    app.router.add_view('/render', RenderView)
