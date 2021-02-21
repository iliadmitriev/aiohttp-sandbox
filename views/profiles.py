from aiohttp import web
from models import Profile
from schemas import profile_schema
from db import get_objects, get_object_by_id, update_object_by_id, insert_object


class ProfilesListView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profiles = await get_objects(conn, Profile)
            result = profile_schema.dump(profiles, many=True)
            return web.json_response(result)

    async def post(self):
        async with self.request.app['db'].acquire() as conn:
            if self.request.content_type == 'application/json':
                data = await self.request.json()
            else:
                data = await self.request.post()
            validated_data = profile_schema.load(data)
            profile = await insert_object(conn, Profile, validated_data)
            result = profile_schema.dump(profile)
            return web.json_response(result)


class ProfilesDetailView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            profile = await get_object_by_id(conn, Profile, profile_id)
            result = profile_schema.dump(profile)
            return web.json_response(result)

    async def patch(self):
        async with self.request.app['db'].acquire() as conn:
            if self.request.content_type == 'application/json':
                data = await self.request.json()
            else:
                data = await self.request.post()
            profile_id = self.request.match_info['profile_id']
            profile = await update_object_by_id(conn, Profile, profile_id, data)
            result = profile_schema.dump(profile)
            return web.json_response(result)
