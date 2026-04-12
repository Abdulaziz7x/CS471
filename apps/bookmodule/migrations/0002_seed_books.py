from django.db import migrations


def seed_books(apps, schema_editor):
    Book = apps.get_model("bookmodule", "Book")
    books = [
        {
            "title": "Continuous Delivery",
            "author": "J. Humble and D. Farley",
            "price": 120.00,
            "edition": 3,
        },
        {
            "title": "Reversing: Secrets of Reverse Engineering",
            "author": "E. Eilam",
            "price": 97.00,
            "edition": 2,
        },
        {
            "title": "The Hundred-Page Machine Learning Book",
            "author": "Andriy Burkov",
            "price": 100.00,
            "edition": 4,
        },
    ]
    for book in books:
        Book.objects.get_or_create(title=book["title"], defaults=book)


def unseed_books(apps, schema_editor):
    Book = apps.get_model("bookmodule", "Book")
    Book.objects.filter(
        title__in=[
            "Continuous Delivery",
            "Reversing: Secrets of Reverse Engineering",
            "The Hundred-Page Machine Learning Book",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("bookmodule", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_books, unseed_books),
    ]
