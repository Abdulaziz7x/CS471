from django.shortcuts import render
from django.http import HttpResponse


BOOKS = [
    {"title": "Clean Code", "author": "Robert C. Martin", "edition": "1st", "price": 125},
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "edition": "4th", "price": 210},
    {"title": "Learning Django", "author": "William S. Vincent", "edition": "4th", "price": 145},
    {"title": "Python Crash Course", "author": "Eric Matthes", "edition": "3rd", "price": 135},
]


def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def search_books(request):
    title = request.GET.get("title", "").strip().lower()
    author = request.GET.get("author", "").strip().lower()

    has_query = bool(title or author)
    results = [
        book for book in BOOKS
        if (not title or title in book["title"].lower())
        and (not author or author in book["author"].lower())
    ] if has_query else []

    return render(
        request,
        "bookmodule/search.html",
        {
            "has_query": has_query,
            "books": results,
            "query": {
                "title": request.GET.get("title", "").strip(),
                "author": request.GET.get("author", "").strip(),
            },
        },
    )


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
