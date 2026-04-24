from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["title", "id"]

    def __str__(self):
        return f"{self.title} by {self.author}"


class Address(models.Model):
    city = models.CharField(max_length=120)

    class Meta:
        ordering = ["city", "id"]

    def __str__(self):
        return self.city


class Student(models.Model):
    name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="students")

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name
