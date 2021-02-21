from aiohttp.web_middlewares import middleware


@middleware
async def server(request, handler):
    return await handler(request)


def setup_middlewares(app):
    app.middlewares.append(server)
