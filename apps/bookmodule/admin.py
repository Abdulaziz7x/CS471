from django.contrib import admin

from .models import Address, Author, Book, Publisher, Student


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "price", "quantity", "rating", "edition")
    list_filter = ("publisher", "rating", "edition")
    search_fields = ("title", "author")
    filter_horizontal = ("authors",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name", "location")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "DOB")
    search_fields = ("name",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("city",)
    search_fields = ("city",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "address")
    list_filter = ("address",)
    search_fields = ("name",)
