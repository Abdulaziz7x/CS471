from django.test import TestCase
from django.urls import reverse


class BookModuleTests(TestCase):
    def test_search_page_loads(self):
        response = self.client.get(reverse("book-search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search for Books")

    def test_search_filters_results(self):
        response = self.client.get(reverse("book-search"), {"title": "django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Learning Django")
