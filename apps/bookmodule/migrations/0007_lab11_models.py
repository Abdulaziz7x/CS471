from django.core.validators import FileExtensionValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookmodule", "0006_seed_lab9_relationships"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address2",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("city", models.CharField(max_length=120)),
            ],
            options={"ordering": ["city", "id"]},
        ),
        migrations.CreateModel(
            name="GalleryItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.FileField(
                        upload_to="gallery/",
                        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["title", "id"]},
        ),
        migrations.CreateModel(
            name="Student2",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("age", models.PositiveIntegerField()),
                ("addresses", models.ManyToManyField(blank=True, related_name="students", to="bookmodule.address2")),
            ],
            options={"ordering": ["name", "id"]},
        ),
    ]
