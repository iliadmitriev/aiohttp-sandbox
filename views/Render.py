from aiohttp_jinja2 import render_template
from aiohttp import web
import pprint


class RenderView(web.View):

    async def get(self):
        """
        ---
        description: This end-point is jinja template rendered
        tags:
        - Render
        produces:
        - text/html
        responses:
            "200":
                description: html page
            "500":
                description: error page
        """
        response = render_template(
            'index.html',
            self.request,
            context={
                'request': pprint.pformat(self.request.__dict__)
            }
        )
        response.headers['content-type'] = 'text/html'
        response.headers['Content-Language'] = 'ru'
        response.headers['Server'] = 'idm'
        return response
