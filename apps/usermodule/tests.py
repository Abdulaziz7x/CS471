from django.test import TestCase
from django.urls import reverse


class UserModuleTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("user-register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Registration")

    def test_register_post_displays_values(self):
        response = self.client.post(
            reverse("user-register"),
            {
                "full_name": "Abdulaziz Omar",
                "email": "aziz@example.com",
                "city": "Riyadh",
                "program": "CS471",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Form submitted successfully.")
        self.assertContains(response, "Abdulaziz Omar")
