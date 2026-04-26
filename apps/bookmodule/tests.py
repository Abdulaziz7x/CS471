from datetime import date, datetime

from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Address, Author, Book, Publisher, Student


class BookModuleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Student.objects.all().delete()
        Address.objects.all().delete()
        Book.objects.all().delete()

        cls.publisher_riyadh = Publisher.objects.create(name="Riyadh Reads", location="Riyadh")
        cls.publisher_jeddah = Publisher.objects.create(name="Jeddah House", location="Jeddah")
        cls.publisher_dammam = Publisher.objects.create(name="Dammam Press", location="Dammam")

        cls.author_humble = Author.objects.create(name="J. Humble and D. Farley", DOB=date(1975, 5, 1))
        cls.author_burkov = Author.objects.create(name="Andriy Burkov", DOB=date(1980, 7, 14))
        cls.author_eilam = Author.objects.create(name="E. Eilam", DOB=date(1972, 3, 2))
        cls.author_lutz = Author.objects.create(name="Mark Lutz", DOB=date(1960, 1, 1))
        cls.author_vincent = Author.objects.create(name="William Vincent", DOB=date(1985, 9, 9))
        cls.author_quinn = Author.objects.create(name="Alice Quinn", DOB=date(1988, 6, 10))
        cls.author_blake = Author.objects.create(name="Quentin Blake", DOB=date(1978, 12, 5))
        cls.author_martin = Author.objects.create(name="Robert Martin", DOB=date(1952, 12, 5))

        cls.create_book(
            title="Continuous Delivery",
            author="J. Humble and D. Farley",
            price=120.0,
            edition=4,
            quantity=7,
            rating=5,
            publisher=cls.publisher_riyadh,
            authors=[cls.author_humble],
            pubdate=datetime(2018, 1, 10, 9, 0, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="The Hundred-Page Machine Learning Book",
            author="Andriy Burkov",
            price=110.0,
            edition=3,
            quantity=5,
            rating=4,
            publisher=cls.publisher_riyadh,
            authors=[cls.author_burkov],
            pubdate=datetime(2019, 5, 20, 11, 0, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="Reversing: Secrets of Reverse Engineering",
            author="E. Eilam",
            price=45.0,
            edition=2,
            quantity=4,
            rating=3,
            publisher=cls.publisher_jeddah,
            authors=[cls.author_eilam],
            pubdate=datetime(2016, 3, 15, 8, 30, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="Learning Python",
            author="Mark Lutz",
            price=75.0,
            edition=5,
            quantity=6,
            rating=5,
            publisher=cls.publisher_jeddah,
            authors=[cls.author_lutz],
            pubdate=datetime(2020, 8, 1, 10, 0, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="Django for APIs",
            author="William Vincent",
            price=65.0,
            edition=2,
            quantity=3,
            rating=4,
            publisher=cls.publisher_dammam,
            authors=[cls.author_vincent],
            pubdate=datetime(2021, 2, 12, 14, 0, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="Quantum Computing Basics",
            author="Alice Quinn",
            price=120.0,
            edition=4,
            quantity=2,
            rating=5,
            publisher=cls.publisher_dammam,
            authors=[cls.author_quinn],
            pubdate=datetime(2017, 11, 30, 16, 0, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="Query Optimization Guide",
            author="Quentin Blake",
            price=90.0,
            edition=6,
            quantity=1,
            rating=2,
            publisher=cls.publisher_riyadh,
            authors=[cls.author_blake],
            pubdate=datetime(2022, 4, 1, 9, 15, tzinfo=timezone.get_current_timezone()),
        )
        cls.create_book(
            title="Clean Code",
            author="Robert Martin",
            price=82.0,
            edition=1,
            quantity=8,
            rating=5,
            publisher=cls.publisher_jeddah,
            authors=[cls.author_martin],
            pubdate=datetime(2015, 7, 7, 13, 45, tzinfo=timezone.get_current_timezone()),
        )

        riyadh = Address.objects.create(city="Riyadh")
        jeddah = Address.objects.create(city="Jeddah")
        dammam = Address.objects.create(city="Dammam")
        Student.objects.create(name="Sara", age=21, address=riyadh)
        Student.objects.create(name="Faisal", age=22, address=riyadh)
        Student.objects.create(name="Lama", age=20, address=jeddah)
        Student.objects.create(name="Nora", age=23, address=dammam)
        Student.objects.create(name="Omar", age=24, address=dammam)

    @classmethod
    def create_book(cls, *, authors, **kwargs):
        book = Book.objects.create(**kwargs)
        book.authors.set(authors)
        return book

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

    def test_simple_query_page_uses_model_results(self):
        response = self.client.get(reverse("simple-query"), {"q": "Book"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Hundred-Page Machine Learning Book")

    def test_complex_query_page_filters_books(self):
        response = self.client.get(
            reverse("complex-query"),
            {"min_price": "100", "min_edition": "3"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continuous Delivery")
        self.assertContains(response, "The Hundred-Page Machine Learning Book")
        self.assertNotContains(response, "Reversing: Secrets of Reverse Engineering")

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
        self.assertEqual(response.context["stats"]["total_books"], 8)
        self.assertEqual(response.context["stats"]["total_price"], 707.0)
        self.assertEqual(response.context["stats"]["maximum_price"], 120.0)
        self.assertEqual(response.context["stats"]["minimum_price"], 45.0)

    def test_lab8_task7_counts_students_per_city(self):
        response = self.client.get(reverse("lab8-task7"))
        self.assertEqual(response.status_code, 200)
        city_counts = {address.city: address.student_count for address in response.context["city_counts"]}
        self.assertEqual(city_counts["Dammam"], 2)
        self.assertEqual(city_counts["Riyadh"], 2)
        self.assertEqual(city_counts["Jeddah"], 1)

    def test_lab9_task1_computes_transient_availability_percentages(self):
        response = self.client.get(reverse("lab9-task1"))
        self.assertEqual(response.status_code, 200)
        books = response.context["books"]
        self.assertEqual(response.context["total_quantity"], 36)
        percentages = {book.title: round(book.availability_percentage, 2) for book in books}
        self.assertEqual(percentages["Continuous Delivery"], 19.44)
        self.assertEqual(percentages["Query Optimization Guide"], 2.78)

    def test_lab9_task2_annotates_total_book_stock_per_publisher(self):
        response = self.client.get(reverse("lab9-task2"))
        self.assertEqual(response.status_code, 200)
        publishers = Publisher.objects.annotate(total=Sum("books__quantity")).order_by("name")
        totals = {publisher.name: publisher.total for publisher in publishers}
        self.assertEqual(totals["Riyadh Reads"], 13)
        self.assertEqual(totals["Jeddah House"], 18)
        self.assertEqual(totals["Dammam Press"], 5)

    def test_lab9_task3_returns_oldest_book_for_each_publisher(self):
        response = self.client.get(reverse("lab9-task3"))
        self.assertEqual(response.status_code, 200)
        publishers = list(response.context["publishers"])
        oldest_titles = {publisher.name: publisher.oldest_book_title for publisher in publishers}
        self.assertEqual(oldest_titles["Riyadh Reads"], "Continuous Delivery")
        self.assertEqual(oldest_titles["Jeddah House"], "Clean Code")
        self.assertEqual(oldest_titles["Dammam Press"], "Quantum Computing Basics")

    def test_lab9_task4_calculates_price_stats_per_publisher(self):
        response = self.client.get(reverse("lab9-task4"))
        self.assertEqual(response.status_code, 200)
        publishers = Publisher.objects.annotate(
            avg_price=Avg("books__price"),
            min_price=Min("books__price"),
            max_price=Max("books__price"),
        )
        stats = {publisher.name: (publisher.avg_price, publisher.min_price, publisher.max_price) for publisher in publishers}
        self.assertEqual(stats["Riyadh Reads"], (106.66666666666667, 90.0, 120.0))
        self.assertEqual(stats["Jeddah House"], (67.33333333333333, 45.0, 82.0))
        self.assertEqual(stats["Dammam Press"], (92.5, 65.0, 120.0))

    def test_lab9_task5_counts_highly_rated_books(self):
        response = self.client.get(reverse("lab9-task5"))
        self.assertEqual(response.status_code, 200)
        publishers = Publisher.objects.annotate(
            highly_rated_books_count=Count("books", filter=Q(books__rating__gte=4), distinct=True),
            highly_rated_books_quantity=Sum("books__quantity", filter=Q(books__rating__gte=4)),
        )
        stats = {
            publisher.name: (
                publisher.highly_rated_books_count,
                publisher.highly_rated_books_quantity,
            )
            for publisher in publishers
        }
        self.assertEqual(stats["Riyadh Reads"], (2, 12))
        self.assertEqual(stats["Jeddah House"], (2, 14))
        self.assertEqual(stats["Dammam Press"], (2, 5))

    def test_lab9_task6_counts_filtered_books_per_publisher(self):
        response = self.client.get(reverse("lab9-task6"))
        self.assertEqual(response.status_code, 200)
        publishers = Publisher.objects.annotate(
            filtered_books_count=Count(
                "books",
                filter=Q(books__price__gt=50, books__quantity__lt=5, books__quantity__gte=1),
                distinct=True,
            )
        )
        stats = {publisher.name: publisher.filtered_books_count for publisher in publishers}
        self.assertEqual(stats["Riyadh Reads"], 1)
        self.assertEqual(stats["Jeddah House"], 0)
        self.assertEqual(stats["Dammam Press"], 2)
