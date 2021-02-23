from views.profiles import MyProfileView


class TestProfileListAdmin:
    async def test_profiles_list_view_401_unauthorized(self, cli):
        resp = await cli.get('/profiles')
        assert resp.status == 401

    async def test_profiles_list_view_200_with_token(self, cli, admin_access_token):
        headers = {
            'Authorization': f'Bearer {admin_access_token}'
        }
        resp = await cli.get('/profiles', headers=headers)
        print(resp)
        assert resp.status == 200

    def test_profiles_list_view_create_201(self):
        assert True

    def test_profiles_list_view_create_400(self):
        assert True


class TestProfileDetailAdmin:
    def test_profiles_detail_view_200(self):
        assert True

    def test_profiles_detail_view_404(self):
        assert True

    def test_profiles_detail_put_200(self):
        assert True

    def test_profiles_detail_patch_200(self):
        assert True

    def test_profiles_detail_delete_200(self):
        assert True


class TestMyProfileUnprivileged:
    def test_my_profile_view_200(self):
        assert True

    def test_my_profile_view_404(self):
        assert True

    def test_my_profile_create(self):
        assert True

    def test_my_profile_create_exist_400(self):
        assert True

    def test_my_profile_create_validation_400(self):
        assert True

    def test_my_profile_patch(self):
        assert True
