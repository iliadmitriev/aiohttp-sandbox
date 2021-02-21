from aiohttp.web_middlewares import middleware
from aiohttp import web
from exceptions import BadRequest, RecordNotFound
from json import JSONDecodeError


async def handle_http_error(request, e, status):
    return web.json_response({'message': str(e)}, status=status)


@middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as e:
        return await handle_http_error(request, str(e), status=e.status)
    except (BadRequest, JSONDecodeError) as e:
        return await handle_http_error(request, str(e), status=400)
    except RecordNotFound as e:
        return await handle_http_error(request, str(e), status=404)
    except Exception as e:
        return await handle_http_error(
            request,
            f'{type(e).__name__}: {str(e)}',
            status=500
        )


def setup_middlewares(app):
    app.middlewares.append(error_middleware)
