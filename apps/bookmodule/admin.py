from django.contrib import admin

from .models import Address, Book, Student


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "edition")
    search_fields = ("title", "author")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("city",)
    search_fields = ("city",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "address")
    list_filter = ("address",)
    search_fields = ("name",)
