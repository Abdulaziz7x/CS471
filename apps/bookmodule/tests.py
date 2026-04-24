from django.test import TestCase
from django.urls import reverse

from .models import Address, Book, Student


class BookModuleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Student.objects.all().delete()
        Address.objects.all().delete()
        Book.objects.all().delete()

        cls.book_python = Book.objects.create(
            title="Learning Python",
            author="Mark Lutz",
            price="75.00",
            edition=5,
        )
        cls.book_django = Book.objects.create(
            title="Django for APIs",
            author="William Vincent",
            price="65.00",
            edition=2,
        )
        cls.book_quantum = Book.objects.create(
            title="Quantum Computing Basics",
            author="Alice Quinn",
            price="120.00",
            edition=4,
        )
        cls.book_query = Book.objects.create(
            title="Query Optimization Guide",
            author="Quentin Blake",
            price="90.00",
            edition=6,
        )
        cls.book_clean = Book.objects.create(
            title="Clean Code",
            author="Robert Martin",
            price="82.00",
            edition=1,
        )

        riyadh = Address.objects.create(city="Riyadh")
        jeddah = Address.objects.create(city="Jeddah")
        Student.objects.create(name="Sara", age=21, address=riyadh)
        Student.objects.create(name="Faisal", age=22, address=riyadh)
        Student.objects.create(name="Lama", age=20, address=jeddah)

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

    def test_lab8_task1_lists_books_priced_up_to_80(self):
        response = self.client.get(reverse("lab8-task1"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Learning Python")
        self.assertContains(response, "Django for APIs")
        self.assertNotContains(response, "Query Optimization Guide")

    def test_lab8_task2_uses_combined_q_queries(self):
        response = self.client.get(reverse("lab8-task2"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quantum Computing Basics")
        self.assertContains(response, "Query Optimization Guide")
        self.assertNotContains(response, "Django for APIs")

    def test_lab8_task3_uses_negated_q_queries(self):
        response = self.client.get(reverse("lab8-task3"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django for APIs")
        self.assertContains(response, "Clean Code")
        self.assertNotContains(response, "Quantum Computing Basics")

    def test_lab8_task4_orders_books_by_title(self):
        response = self.client.get(reverse("lab8-task4"))
        self.assertEqual(response.status_code, 200)
        books = list(response.context["books"])
        self.assertEqual(
            [book.title for book in books],
            sorted(book.title for book in books),
        )

    def test_lab8_task5_shows_aggregates(self):
        response = self.client.get(reverse("lab8-task5"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["stats"]["total_books"], 5)
        self.assertContains(response, "432")
        self.assertContains(response, "120")
        self.assertContains(response, "65")

    def test_lab8_task7_counts_students_per_city(self):
        response = self.client.get(reverse("lab8-task7"))
        self.assertEqual(response.status_code, 200)
        city_counts = {address.city: address.student_count for address in response.context["city_counts"]}
        self.assertEqual(city_counts["Riyadh"], 2)
        self.assertEqual(city_counts["Jeddah"], 1)
