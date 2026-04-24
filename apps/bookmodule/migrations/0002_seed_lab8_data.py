from decimal import Decimal

from django.db import migrations


BOOKS = [
    {"title": "Learning Python", "author": "Mark Lutz", "price": Decimal("75.00"), "edition": 5},
    {"title": "Django for APIs", "author": "William Vincent", "price": Decimal("65.00"), "edition": 2},
    {"title": "Quantum Computing Basics", "author": "Alice Quinn", "price": Decimal("120.00"), "edition": 4},
    {"title": "Query Optimization Guide", "author": "Quentin Blake", "price": Decimal("90.00"), "edition": 6},
    {"title": "Clean Code", "author": "Robert Martin", "price": Decimal("82.00"), "edition": 1},
    {"title": "Deep Learning Illustrated", "author": "Jon Krohn", "price": Decimal("79.99"), "edition": 3},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "price": Decimal("68.50"), "edition": 4},
    {"title": "Square Patterns in CSS", "author": "Mia Stone", "price": Decimal("54.00"), "edition": 2},
]

ADDRESSES = ["Riyadh", "Jeddah", "Dammam"]

STUDENTS = [
    {"name": "Sara Almutairi", "age": 21, "city": "Riyadh"},
    {"name": "Faisal Alqahtani", "age": 22, "city": "Riyadh"},
    {"name": "Lama Alharbi", "age": 20, "city": "Jeddah"},
    {"name": "Nora Alshammari", "age": 23, "city": "Dammam"},
    {"name": "Omar Alshehri", "age": 24, "city": "Dammam"},
]


def seed_forward(apps, schema_editor):
    Book = apps.get_model("bookmodule", "Book")
    Address = apps.get_model("bookmodule", "Address")
    Student = apps.get_model("bookmodule", "Student")

    for book in BOOKS:
        Book.objects.get_or_create(
            title=book["title"],
            defaults={
                "author": book["author"],
                "price": book["price"],
                "edition": book["edition"],
            },
        )

    address_map = {}
    for city in ADDRESSES:
        address, _ = Address.objects.get_or_create(city=city)
        address_map[city] = address

    for student in STUDENTS:
        Student.objects.get_or_create(
            name=student["name"],
            defaults={
                "age": student["age"],
                "address": address_map[student["city"]],
            },
        )


def seed_reverse(apps, schema_editor):
    Book = apps.get_model("bookmodule", "Book")
    Address = apps.get_model("bookmodule", "Address")
    Student = apps.get_model("bookmodule", "Student")

    Student.objects.filter(name__in=[student["name"] for student in STUDENTS]).delete()
    Address.objects.filter(city__in=ADDRESSES).delete()
    Book.objects.filter(title__in=[book["title"] for book in BOOKS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bookmodule", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
