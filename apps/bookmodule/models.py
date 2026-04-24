from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    edition = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


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
