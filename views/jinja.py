from aiohttp_jinja2 import template
from aiohttp import web


class JinjaView(web.View):

    @template('jinja.html', status=200)
    async def get(self):
        """
        ---
        description: This end-point is rendered by Jinja2 template
        tags:
        - Jinja2
        produces:
        - text/html
        responses:
            "200":
                description: Rendered html code
        """
        return {}
