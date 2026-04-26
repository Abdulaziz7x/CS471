from datetime import date, datetime

from django.db import migrations
from django.utils import timezone


PUBLISHERS = [
    {"name": "Riyadh Reads", "location": "Riyadh"},
    {"name": "Jeddah House", "location": "Jeddah"},
    {"name": "Dammam Press", "location": "Dammam"},
]

AUTHORS = [
    {"name": "J. Humble and D. Farley", "DOB": date(1975, 5, 1)},
    {"name": "Andriy Burkov", "DOB": date(1980, 7, 14)},
    {"name": "E. Eilam", "DOB": date(1972, 3, 2)},
    {"name": "Mark Lutz", "DOB": date(1960, 1, 1)},
    {"name": "William Vincent", "DOB": date(1985, 9, 9)},
    {"name": "Alice Quinn", "DOB": date(1988, 6, 10)},
    {"name": "Quentin Blake", "DOB": date(1978, 12, 5)},
    {"name": "Robert Martin", "DOB": date(1952, 12, 5)},
]

BOOKS = [
    {
        "title": "Continuous Delivery",
        "author": "J. Humble and D. Farley",
        "price": 120.0,
        "edition": 4,
        "quantity": 7,
        "rating": 5,
        "publisher": "Riyadh Reads",
        "authors": ["J. Humble and D. Farley"],
        "pubdate": datetime(2018, 1, 10, 9, 0),
    },
    {
        "title": "The Hundred-Page Machine Learning Book",
        "author": "Andriy Burkov",
        "price": 110.0,
        "edition": 3,
        "quantity": 5,
        "rating": 4,
        "publisher": "Riyadh Reads",
        "authors": ["Andriy Burkov"],
        "pubdate": datetime(2019, 5, 20, 11, 0),
    },
    {
        "title": "Reversing: Secrets of Reverse Engineering",
        "author": "E. Eilam",
        "price": 45.0,
        "edition": 2,
        "quantity": 4,
        "rating": 3,
        "publisher": "Jeddah House",
        "authors": ["E. Eilam"],
        "pubdate": datetime(2016, 3, 15, 8, 30),
    },
    {
        "title": "Learning Python",
        "author": "Mark Lutz",
        "price": 75.0,
        "edition": 5,
        "quantity": 6,
        "rating": 5,
        "publisher": "Jeddah House",
        "authors": ["Mark Lutz"],
        "pubdate": datetime(2020, 8, 1, 10, 0),
    },
    {
        "title": "Django for APIs",
        "author": "William Vincent",
        "price": 65.0,
        "edition": 2,
        "quantity": 3,
        "rating": 4,
        "publisher": "Dammam Press",
        "authors": ["William Vincent"],
        "pubdate": datetime(2021, 2, 12, 14, 0),
    },
    {
        "title": "Quantum Computing Basics",
        "author": "Alice Quinn",
        "price": 120.0,
        "edition": 4,
        "quantity": 2,
        "rating": 5,
        "publisher": "Dammam Press",
        "authors": ["Alice Quinn"],
        "pubdate": datetime(2017, 11, 30, 16, 0),
    },
    {
        "title": "Query Optimization Guide",
        "author": "Quentin Blake",
        "price": 90.0,
        "edition": 6,
        "quantity": 1,
        "rating": 2,
        "publisher": "Riyadh Reads",
        "authors": ["Quentin Blake"],
        "pubdate": datetime(2022, 4, 1, 9, 15),
    },
    {
        "title": "Clean Code",
        "author": "Robert Martin",
        "price": 82.0,
        "edition": 1,
        "quantity": 8,
        "rating": 5,
        "publisher": "Jeddah House",
        "authors": ["Robert Martin"],
        "pubdate": datetime(2015, 7, 7, 13, 45),
    },
]


def seed_forward(apps, schema_editor):
    Publisher = apps.get_model("bookmodule", "Publisher")
    Author = apps.get_model("bookmodule", "Author")
    Book = apps.get_model("bookmodule", "Book")

    publisher_map = {}
    for publisher_data in PUBLISHERS:
        publisher, _ = Publisher.objects.get_or_create(
            name=publisher_data["name"],
            defaults={"location": publisher_data["location"]},
        )
        publisher.location = publisher_data["location"]
        publisher.save(update_fields=["location"])
        publisher_map[publisher.name] = publisher

    author_map = {}
    for author_data in AUTHORS:
        author, _ = Author.objects.get_or_create(
            name=author_data["name"],
            defaults={"DOB": author_data["DOB"]},
        )
        author.DOB = author_data["DOB"]
        author.save(update_fields=["DOB"])
        author_map[author.name] = author

    for book_data in BOOKS:
        book = Book.objects.get(title=book_data["title"])
        book.author = book_data["author"]
        book.price = book_data["price"]
        book.edition = book_data["edition"]
        book.quantity = book_data["quantity"]
        book.rating = book_data["rating"]
        book.publisher = publisher_map[book_data["publisher"]]
        book.pubdate = timezone.make_aware(book_data["pubdate"], timezone.get_current_timezone())
        book.save()
        book.authors.set([author_map[name] for name in book_data["authors"]])


def seed_reverse(apps, schema_editor):
    Publisher = apps.get_model("bookmodule", "Publisher")
    Author = apps.get_model("bookmodule", "Author")
    Book = apps.get_model("bookmodule", "Book")

    for book_data in BOOKS:
        try:
            book = Book.objects.get(title=book_data["title"])
        except Book.DoesNotExist:
            continue

        book.authors.clear()
        book.publisher = None
        book.quantity = 1
        book.rating = 1
        book.save(update_fields=["publisher", "quantity", "rating"])

    Author.objects.filter(name__in=[author["name"] for author in AUTHORS]).delete()
    Publisher.objects.filter(name__in=[publisher["name"] for publisher in PUBLISHERS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bookmodule", "0005_author_publisher_alter_book_options_book_pubdate_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
