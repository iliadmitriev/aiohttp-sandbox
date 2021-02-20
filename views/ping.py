from aiohttp import web


class PingView(web.View):

    async def get(self):
        """
        ---
        description: This end-point allow to test that service is up.
        tags:
        - Ping
        produces:
        - application/json
        responses:
            "200":
                description: successful operation. Return "pong" text
            "405":
                description: invalid HTTP Method
        """
        return web.json_response({'ping': 'Ok'})

    async def delete(self):
        """
        ---
        description: This end-point allow to test that service is up.
        tags:
        - Ping
        produces:
        - application/json
        responses:
            "405":
                description: invalid HTTP Method
        """
        return web.json_response({'message': 'fail'}, status=405)

