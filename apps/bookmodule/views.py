from django.shortcuts import render
from django.http import HttpResponse

from .models import Book


BOOKS = [
    {"id": 12344321, "title": "Continuous Delivery", "author": "J. Humble and D. Farley"},
    {"id": 56788765, "title": "Reverse Engineering", "author": "E. Eilam"},
    {"id": 42311234, "title": "The Hundred-Page Machine Learning Book", "author": "Andriy Burkov"},
]


def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def searchbooks(request):
    if request.method == "POST":
        string = request.POST.get("keyword", "").lower()
        is_title = request.POST.get("title")
        is_author = request.POST.get("author")

        newBooks = []
        for item in BOOKS:
            contained = False
            if is_title and string in item["title"].lower():
                contained = True
            if is_author and string in item["author"].lower():
                contained = True
            if contained:
                newBooks.append(item)

        return render(request, "bookmodule/bookList.html", {"books": newBooks})

    return render(request, "bookmodule/search.html")


def simple_query(request):
    query_text = request.GET.get("q", "Book").strip()
    books = Book.objects.filter(title__icontains=query_text)
    return render(
        request,
        "bookmodule/bookList.html",
        {"books": books, "query_text": query_text, "mode": "simple"},
    )


def complex_query(request):
    min_price = request.GET.get("min_price", "100").strip()
    min_edition = request.GET.get("min_edition", "2").strip()

    try:
        min_price_value = float(min_price)
    except ValueError:
        min_price_value = 100.0

    try:
        min_edition_value = int(min_edition)
    except ValueError:
        min_edition_value = 2

    books = Book.objects.filter(
        price__gte=min_price_value,
        edition__gte=min_edition_value,
    ).order_by("-price", "-edition", "title")

    return render(
        request,
        "bookmodule/complexList.html",
        {
            "books": books,
            "min_price": min_price_value,
            "min_edition": min_edition_value,
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
