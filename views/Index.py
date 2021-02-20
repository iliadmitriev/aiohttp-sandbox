from aiohttp.web import View
from aiohttp import web
import json


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
            'status': 'success'
        }
        headers = {
            'content-type': 'application/json'
        }
        return web.Response(
            text=json.dumps(
                response_obj,
                sort_keys=True,
                indent=4
            ),
            status=200,
            headers=headers
        )

