from aiohttp import web
from sqlalchemy.sql import select
from models import Profile
from db import get_objects, get_object_by_id, update_object_by_id, insert_object


class ProfilesListView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profiles = await get_objects(conn, Profile)
            return web.json_response(profiles)

    async def post(self):
        async with self.request.app['db'].acquire() as conn:
            data = await self.request.post()
            profile = await insert_object(conn, Profile, data)
            return web.json_response(dict(profile))


class ProfilesDetailView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            profile = await get_object_by_id(conn, Profile, profile_id)
            return web.json_response(dict(profile))

    async def patch(self):
        async with self.request.app['db'].acquire() as conn:
            data = await self.request.post()
            profile_id = self.request.match_info['profile_id']
            profile = await update_object_by_id(conn, Profile, profile_id, data)
            return web.json_response(dict(profile))
