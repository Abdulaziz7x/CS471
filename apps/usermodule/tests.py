from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserModuleTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("user-register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_register_post_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("user-register"),
            {
                "username": "abdulaziz",
                "email": "aziz@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="abdulaziz").exists())
        self.assertContains(response, "You have successfully registered.")

    def test_login_page_loads(self):
        response = self.client.get(reverse("user-login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_login_post_authenticates_user(self):
        User.objects.create_user(username="lab12user", password="StrongPass123!")
        response = self.client.post(
            reverse("user-login"),
            {"username": "lab12user", "password": "StrongPass123!"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="lab12user").id)
        self.assertContains(response, "Login successfully.")

    def test_logout_clears_authenticated_session(self):
        user = User.objects.create_user(username="logoutuser", password="StrongPass123!")
        self.client.force_login(user)
        response = self.client.get(reverse("user-logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "You have successfully logged out.")
