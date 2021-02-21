from aiohttp import web
from sqlalchemy.sql import select
from models import Profile
from db import get_object_by_id, RecordNotFound


class ProfilesListView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            cursor = await conn.execute(select([Profile]))
            records = await cursor.fetchall()
            profiles = [dict(p) for p in records]
            return web.json_response(profiles)


class ProfilesDetailView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            try:
                profile = await get_object_by_id(conn, Profile, profile_id)
            except RecordNotFound as e:
                return web.json_response({'error': str(e)}, status=404)
            return web.json_response({
                'id': profile.id,
                'firstname': profile.firstname,
                'surname': profile.surname,
                'user_id': profile.user_id
            })
