from django.db import migrations


ADDRESSES = ["Riyadh", "Jeddah", "Dammam"]


def seed_forward(apps, schema_editor):
    Address2 = apps.get_model("bookmodule", "Address2")
    for city in ADDRESSES:
        Address2.objects.get_or_create(city=city)


def seed_reverse(apps, schema_editor):
    Address2 = apps.get_model("bookmodule", "Address2")
    Address2.objects.filter(city__in=ADDRESSES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bookmodule", "0007_lab11_models"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
