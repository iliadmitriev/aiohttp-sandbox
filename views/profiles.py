from aiohttp import web
from aiohttp_jwt import check_permissions, match_any, login_required
from models import Profile
from schemas import profile_schema, my_profile_schema
from db import (
    get_objects,
    get_object_by_id,
    get_object_by_user_id,
    update_object_by_id,
    update_object_by_user_id,
    insert_object,
    delete_object_by_id
)


class MyProfileView(web.View):
    @login_required
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            user_id = self.request['user']['user_id']
            profile = await get_object_by_user_id(conn, Profile, user_id)
            result = my_profile_schema.dump(profile)
            return web.json_response(result)

    @login_required
    async def post(self):
        async with self.request.app['db'].acquire() as conn:
            if self.request.content_type == 'application/json':
                data = await self.request.json()
            else:
                data = await self.request.post()
            validated_data = my_profile_schema.load(data)
            validated_data['user_id'] = self.request['user']['user_id']
            profile = await insert_object(conn, Profile, validated_data)
            result = my_profile_schema.dump(profile)
            return web.json_response(result, status=201)

    @login_required
    async def patch(self):
        async with self.request.app['db'].acquire() as conn:
            if self.request.content_type == 'application/json':
                data = await self.request.json()
            else:
                data = await self.request.post()
            user_id = self.request['user']['user_id']
            validated_data = my_profile_schema.load(data, partial=True)
            validated_data['user_id'] = user_id
            profile = await update_object_by_user_id(conn, Profile, user_id, validated_data)
            result = my_profile_schema.dump(profile)
            return web.json_response(result)


class ProfilesListView(web.View):
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profiles = await get_objects(conn, Profile)
            result = profile_schema.dump(profiles, many=True)
            return web.json_response(result)

    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def post(self):
        async with self.request.app['db'].acquire() as conn:
            if self.request.content_type == 'application/json':
                data = await self.request.json()
            else:
                data = await self.request.post()
            validated_data = profile_schema.load(data)
            profile = await insert_object(conn, Profile, validated_data)
            result = profile_schema.dump(profile)
            return web.json_response(result, status=201)


class ProfilesDetailView(web.View):
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            profile = await get_object_by_id(conn, Profile, profile_id)
            result = profile_schema.dump(profile)
            return web.json_response(result)

    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def update(self, partial):
        async with self.request.app['db'].acquire() as conn:
            if self.request.content_type == 'application/json':
                data = await self.request.json()
            else:
                data = await self.request.post()
            profile_id = self.request.match_info['profile_id']
            validated_data = profile_schema.load(data, partial=partial)
            profile = await update_object_by_id(conn, Profile, profile_id, validated_data)
            result = profile_schema.dump(profile)
            return web.json_response(result)

    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def put(self):
        return await self.update(partial=False)

    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def patch(self):
        return await self.update(partial=True)

    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def delete(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            profile = await delete_object_by_id(conn, Profile, profile_id)
            result = profile_schema.dump(profile)
            return web.json_response(result)
