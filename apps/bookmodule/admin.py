from django.contrib import admin

from .models import Address, Address2, Author, Book, GalleryItem, Publisher, Student, Student2


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


@admin.register(Address2)
class Address2Admin(admin.ModelAdmin):
    list_display = ("city",)
    search_fields = ("city",)


@admin.register(Student2)
class Student2Admin(admin.ModelAdmin):
    list_display = ("name", "age")
    search_fields = ("name",)
    filter_horizontal = ("addresses",)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")
