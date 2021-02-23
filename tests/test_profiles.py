from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from db import insert_object
from schemas import profile_schema
from views.profiles import Profile
import json
import pytest

from tests.conftest import (
    get_admin_access_token,
    get_unprivileged_access_token
)


@pytest.mark.usefixtures('dsn')
class AioHTTPTestCaseWithTestDB(AioHTTPTestCase):
    admin_access_token = get_admin_access_token(user_id=100)
    unprivileged_access_token = get_unprivileged_access_token(user_id=200)
    unprivileged_access_token_404 = get_unprivileged_access_token(user_id=404)

    async def get_application(self):
        from routes import setup_routes
        from middlewares import setup_middlewares
        from db import setup_db
        app = web.Application()
        setup_routes(app)
        setup_middlewares(app)
        setup_db(app, self.dsn)
        self.app = app
        return app


class TestProfileListAdmin(AioHTTPTestCaseWithTestDB):

    @unittest_run_loop
    async def test_profiles_list_view_401_unauthorized(self):
        resp = await self.client.get('/profiles')
        assert resp.status == 401

    @unittest_run_loop
    async def test_profiles_list_view_200_with_token(self):
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        resp = await self.client.get('/profiles', headers=headers)
        assert resp.status == 200

    @unittest_run_loop
    async def test_profiles_list_view_create_201(self):
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        data = {
            'firstname': 'ivan',
            'surname': 'petrov',
            'birthdate': '1990-02-04',
            'user_id': 2000
        }
        resp = await self.client.post('/profiles', headers=headers, data=data)
        assert resp.status == 201

    @unittest_run_loop
    async def test_profiles_list_view_create_json_201(self):
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'firstname': 'ivan',
            'surname': 'petrov',
            'birthdate': '1990-02-04',
            'user_id': 1777
        }
        resp = await self.client.post(
            '/profiles', headers=headers,
            data=json.dumps(data)
        )
        assert resp.status == 201

    @unittest_run_loop
    async def test_profiles_list_view_create_400(self):
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        data = {
            'user_id': 2000
        }
        resp = await self.client.post('/profiles', headers=headers, data=data)
        assert resp.status == 400


class TestProfileDetailAdmin(AioHTTPTestCaseWithTestDB):

    @unittest_run_loop
    async def test_profiles_detail_view_200(self):
        async with self.app['db'].acquire() as conn:
            validated_data = profile_schema.load({
                'firstname': 'ivan',
                'surname': 'petrov',
                'birthdate': '1990-02-04',
                'user_id': 2001
            })
            profile = await insert_object(conn, Profile, validated_data)
            pr = profile_schema.dump(profile)

        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        resp = await self.client.get(f'/profiles/{pr["id"]}', headers=headers)
        assert resp.status == 200

    @unittest_run_loop
    async def test_profiles_detail_view_404(self):
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        resp = await self.client.get('/profiles/1999', headers=headers)
        assert resp.status == 404

    @unittest_run_loop
    async def test_profiles_detail_put_200(self):
        async with self.app['db'].acquire() as conn:
            validated_data = profile_schema.load({
                'firstname': 'ivan',
                'surname': 'petrov',
                'birthdate': '1990-02-04',
                'user_id': 2002
            })
            profile = await insert_object(conn, Profile, validated_data)
            pr = profile_schema.dump(profile)

        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        data = {
            'firstname': 'ivan',
            'surname': 'petrov',
            'birthdate': '1990-02-04',
            'user_id': 2003
        }
        resp = await self.client.put(f'/profiles/{pr["id"]}', headers=headers, data=data)
        assert resp.status == 200

    @unittest_run_loop
    async def test_profiles_detail_patch_200(self):
        async with self.app['db'].acquire() as conn:
            validated_data = profile_schema.load({
                'firstname': 'ivan',
                'surname': 'smirnov',
                'birthdate': '1990-02-04',
                'user_id': 2004
            })
            profile = await insert_object(conn, Profile, validated_data)
            pr = profile_schema.dump(profile)
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'birthdate': '1994-02-04',
        }
        resp = await self.client.patch(
            f'/profiles/{pr["id"]}', headers=headers,
            data=json.dumps(data)
        )
        assert resp.status == 200

    @unittest_run_loop
    async def test_profiles_detail_delete_200(self):
        async with self.app['db'].acquire() as conn:
            validated_data = profile_schema.load({
                'firstname': 'ivan',
                'surname': 'smirnov',
                'birthdate': '1990-02-04',
                'user_id': 2005
            })
            profile = await insert_object(conn, Profile, validated_data)
            pr = profile_schema.dump(profile)
        headers = {
            'Authorization': f'Bearer {self.admin_access_token}'
        }
        resp = await self.client.delete(f'/profiles/{pr["id"]}', headers=headers)
        assert resp.status == 200


class TestMyProfileUnprivileged(AioHTTPTestCaseWithTestDB):
    @unittest_run_loop
    async def test_my_profile_view_404(self):
        headers = {
            'Authorization': f'Bearer {self.unprivileged_access_token_404}'
        }
        resp = await self.client.get('/my-profile', headers=headers)
        assert resp.status == 404

    @unittest_run_loop
    async def test_my_profile_create(self):
        headers = {
            'Authorization': f'Bearer {self.unprivileged_access_token}'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged',
            'birthdate': '1991-05-08'
        }
        resp = await self.client.post('/my-profile', headers=headers, data=data)
        assert resp.status == 201

    @unittest_run_loop
    async def test_my_profile_create_post_json(self):
        headers = {
            'Authorization': f'Bearer {get_unprivileged_access_token(user_id=16)}',
            'Content-Type': 'application/json'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged',
            'birthdate': '1991-05-08'
        }
        resp = await self.client.post(
            '/my-profile',
            headers=headers,
            data=json.dumps(data)
        )
        assert resp.status == 201

    @unittest_run_loop
    async def test_my_profile_view_200(self):
        headers = {
            'Authorization': f'Bearer {self.unprivileged_access_token}'
        }
        resp = await self.client.get('/my-profile', headers=headers)
        assert resp.status == 200

    @unittest_run_loop
    async def test_my_profile_create_exist_400(self):
        token = get_unprivileged_access_token(user_id=55)
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged',
            'birthdate': '1991-05-08'
        }
        resp = await self.client.post('/my-profile', headers=headers, data=data)
        assert resp.status == 201
        token = get_unprivileged_access_token(user_id=55)
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged',
            'birthdate': '1991-05-08'
        }
        resp = await self.client.post('/my-profile', headers=headers, data=data)
        assert resp.status == 400

    @unittest_run_loop
    async def test_my_profile_create_validation_400(self):
        token = get_unprivileged_access_token(user_id=77)
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged',
            'birthdate': 'invalid',
            'gender': 'invalid'
        }
        resp = await self.client.post('/my-profile', headers=headers, data=data)
        assert resp.status == 400

    @unittest_run_loop
    async def test_my_profile_patch(self):
        token = get_unprivileged_access_token(user_id=88)
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged'
        }
        resp = await self.client.post('/my-profile', headers=headers, data=data)
        assert resp.status == 201
        token = get_unprivileged_access_token(user_id=88)
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {
            'birthdate': '1990-01-01',
            'gender': 'male'
        }
        resp = await self.client.patch('/my-profile', headers=headers, data=data)
        assert resp.status == 200

    @unittest_run_loop
    async def test_my_profile_patch_post_json(self):
        token = get_unprivileged_access_token(user_id=177)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        data = {
            'firstname': 'user',
            'surname': 'unprivileged'
        }
        resp = await self.client.post(
            '/my-profile', headers=headers,
            data=json.dumps(data)
        )
        assert resp.status == 201
        token = get_unprivileged_access_token(user_id=88)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        data = {
            'birthdate': '1990-01-01',
            'gender': 'male'
        }
        resp = await self.client.patch(
            '/my-profile', headers=headers,
            data=json.dumps(data)
        )
        assert resp.status == 200
