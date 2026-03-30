from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def viewbook(request, bookId):
    book1 = {"id": 123, "title": "Continuous Delivery", "author": "J. Humble and D. Farley"}
    book2 = {"id": 456, "title": "Secrets of Reverse Engineering", "author": "E. Eilam"}

    targetBook = None
    if book1["id"] == bookId:
        targetBook = book1
    if book2["id"] == bookId:
        targetBook = book2

    context = {"book": targetBook}
    return render(request, "bookmodule/show.html", context)


def lab5_links(request):
    return render(request, "bookmodule/links.html", {"page_title": "Lab 5 - Links"})


def lab5_formatting(request):
    return render(request, "bookmodule/formatting.html", {"page_title": "Lab 5 - Formatting"})


def lab5_listing(request):
    return render(request, "bookmodule/listing.html", {"page_title": "Lab 5 - Listing"})


def lab5_tables(request):
    return render(request, "bookmodule/tables.html", {"page_title": "Lab 5 - Tables"})
