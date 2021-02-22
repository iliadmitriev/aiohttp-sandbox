from views.render import RenderView
from views.index import IndexView
from views.ping import PingView
from views.jinja import JinjaView
from views.profiles import ProfilesListView, ProfilesDetailView, MyProfileView


def setup_routes(app):
    app.router.add_view('/jinja', JinjaView)
    app.router.add_view('/ping', PingView)
    app.router.add_view('/', IndexView)
    app.router.add_view('/render', RenderView)
    app.router.add_view('/profiles', ProfilesListView)
    app.router.add_view('/profiles/{profile_id}', ProfilesDetailView)
    app.router.add_view('/my-profile', MyProfileView)
