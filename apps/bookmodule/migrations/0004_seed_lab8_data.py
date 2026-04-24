from django.db import migrations


BOOKS = [
    {
        "title": "Continuous Delivery",
        "author": "J. Humble and D. Farley",
        "price": 120.0,
        "edition": 4,
    },
    {
        "title": "The Hundred-Page Machine Learning Book",
        "author": "Andriy Burkov",
        "price": 110.0,
        "edition": 3,
    },
    {
        "title": "Reversing: Secrets of Reverse Engineering",
        "author": "E. Eilam",
        "price": 45.0,
        "edition": 2,
    },
    {
        "title": "Learning Python",
        "author": "Mark Lutz",
        "price": 75.0,
        "edition": 5,
    },
    {
        "title": "Django for APIs",
        "author": "William Vincent",
        "price": 65.0,
        "edition": 2,
    },
    {
        "title": "Quantum Computing Basics",
        "author": "Alice Quinn",
        "price": 120.0,
        "edition": 4,
    },
    {
        "title": "Query Optimization Guide",
        "author": "Quentin Blake",
        "price": 90.0,
        "edition": 6,
    },
    {
        "title": "Clean Code",
        "author": "Robert Martin",
        "price": 82.0,
        "edition": 1,
    },
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
        ("bookmodule", "0003_address_student_models"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
