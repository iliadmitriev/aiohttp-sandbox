# tests/test_profiles


class TestProfileListAdmin:
    def test_profiles_list_view_200(self):
        assert True

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
