from aiohttp import web
from aiohttp_jwt import check_permissions, match_any, login_required
from models import Profile
from schemas import (
    profile_schema,
    my_profile_schema,
    MyProfileSchema,
    ProfileSchema,
    default_profile_responses
    )
from db import (
    get_objects,
    get_object_by_id,
    get_object_by_user_id,
    update_object_by_id,
    update_object_by_user_id,
    insert_object,
    delete_object_by_id
)
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema
)

default_parameters = [{
    'in': 'header',
    'name': 'Authorization',
    'type': 'string',
    'format': 'Bearer',
    'required': 'true'
}]


class MyProfileView(web.View):
    @response_schema(MyProfileSchema())
    @docs(
        tags=['authorized'],
        summary="Personal profile get method",
        description="This method is used by unprivileged "
                    "users to get their profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": MyProfileSchema(),
            },
        }
    )
    @login_required
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            user_id = self.request['user']['user_id']
            profile = await get_object_by_user_id(conn, Profile, user_id)
            result = my_profile_schema.dump(profile)
            return web.json_response(result)

    @docs(
        tags=['authorized'],
        summary="Personal profile create method",
        description="This method is used by unprivileged "
                    "users only once to create their profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            201: {
                "description": "Success",
                "schema": MyProfileSchema()
            },
        }
    )
    @request_schema(MyProfileSchema())
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

    @docs(
        tags=['authorized'],
        summary="Personal profile partial update method",
        description="This method is used by unprivileged "
                    "users for partial data update in their profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": MyProfileSchema(),
            },
        }
    )
    @request_schema(MyProfileSchema())
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
    @docs(
        tags=['superuser'],
        summary="Profiles list method",
        parameters=default_parameters,
        description="This methods is used by administrators "
                    "to get a list of users profiles",
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": ProfileSchema(many=True),
            },
        }
    )
    @response_schema(ProfileSchema(many=True))
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profiles = await get_objects(conn, Profile)
            result = profile_schema.dump(profiles, many=True)
            return web.json_response(result)

    @docs(
        tags=['superuser'],
        summary="Profiles create",
        description="This methods is used by administrators "
                    "to create users profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            201: {
                "description": "Success",
                "schema": ProfileSchema(),
            },
        }
    )
    @request_schema(ProfileSchema())
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
    @docs(
        tags=['superuser'],
        summary="Get profile details",
        description="This methods is used by administrators "
                    "to get users profile detail",
        parameters=default_parameters,
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": ProfileSchema(),
            },
        }
    )
    @response_schema(ProfileSchema())
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            profile = await get_object_by_id(conn, Profile, profile_id)
            result = profile_schema.dump(profile)
            return web.json_response(result)

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

    @docs(
        tags=['superuser'],
        summary="Full update of all profile fields",
        description="This methods is used by administrators "
                    "to update users profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": ProfileSchema(),
            },
        }
    )
    @request_schema(ProfileSchema())
    @response_schema(ProfileSchema())
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def put(self):
        return await self.update(partial=False)

    @docs(
        tags=['superuser'],
        summary="Partial update of profile fields",
        description="This methods is used by administrators "
                    "to update profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": ProfileSchema(),
            },
        }
    )
    @request_schema(ProfileSchema())
    @response_schema(ProfileSchema())
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def patch(self):
        return await self.update(partial=True)

    @docs(
        tags=['superuser'],
        summary="Delete profiles",
        description="This methods is used by administrators "
                    "to delete users profiles",
        parameters=default_parameters,
        responses=default_profile_responses | {
            200: {
                "description": "Success",
                "schema": ProfileSchema(),
            },
        }
    )
    @response_schema(ProfileSchema())
    @login_required
    @check_permissions('admin', 'scope', comparison=match_any)
    async def delete(self):
        async with self.request.app['db'].acquire() as conn:
            profile_id = self.request.match_info['profile_id']
            profile = await delete_object_by_id(conn, Profile, profile_id)
            result = profile_schema.dump(profile)
            return web.json_response(result)
