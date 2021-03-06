from aiohttp.web import View
from aiohttp import web


class IndexView(View):

    async def get(self):
        """
        ---
        description: This end-point is index page
        tags:
        - Index
        produces:
        - application/json
        responses:
            "200":
                description: json response with  `status`
        """
        response_obj = {
            'status': 'success',
            'headers': dict(self.request.headers)
        }
        return web.json_response(response_obj)

