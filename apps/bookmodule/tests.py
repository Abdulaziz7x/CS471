from django.test import TestCase
from django.urls import reverse


class BookModuleTests(TestCase):
    def test_search_page_loads(self):
        response = self.client.get(reverse("book-search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Searching Page")
        self.assertContains(response, 'method="post"', html=False)
        self.assertContains(response, 'name="keyword"', html=False)

    def test_search_filters_results(self):
        response = self.client.post(
            reverse("book-search"),
            {"keyword": "delivery", "title": "on"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Books List")
        self.assertContains(response, "Continuous Delivery")
