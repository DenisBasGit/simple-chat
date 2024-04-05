from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.users.factory import UserFactory


class TestAuthorizationAPITestCase(APITestCase):
    """AuthorizationAPITest"""

    def setUp(self) -> None:
        self.url = reverse("api:users_app:login")

    def test_reverse_url(self):
        """test_reverse_url"""
        url = "/api/v1/users/login/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_login_empty_data(self):
        """test_login_with_no_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_pass(self):
        """test_login_wrong_password"""
        user = UserFactory(is_active=True)
        data = {"username": user.username, "password": "WrongPassword123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_wrong_credentials(self):
        """test_login_with_wrong_credentials"""
        data = {"username": "not_exists_user", "password": "WrongPassword123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_not_active(self):
        """test_login_when_user_is_not_active"""
        user = UserFactory(is_active=False)
        data = {"username": user.username, "password": "GoodPassword123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        """test_login_success"""
        user = UserFactory(is_active=True)
        password = "password"
        user.set_password(password)
        user.save()
        data = {
            "username": user.username,
            "password": password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRefreshTokenAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("api:users_app:refresh")
        login_url = reverse("api:users_app:login")
        data = {
            "username": self.user.username,
            "password": self.password,
        }
        response = self.client.post(login_url, data)
        self.data = response.data

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_active=True)
        cls.password = "password"
        cls.user.set_password(cls.password)
        cls.user.save(update_fields=["password"])

    def test_reverse_url(self):
        """test_reverse_url"""
        url = "/api/v1/users/refresh/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_refresh_empty_data(self):
        """test_obtain_token_with_empty_data"""
        data = {"refresh": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_with_correct_data(self):
        """test_obtain_token_pair_success"""
        data = {"refresh": self.data["refresh"]}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_with_corrupted_data(self):
        """test_obtain_token_pair_with_corrupted_data"""
        data = {"refresh": self.data["refresh"] + "123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
