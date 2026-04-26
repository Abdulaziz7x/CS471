from django.db.models import Avg, Count, Max, Min, OuterRef, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render

from .models import Address, Book, Publisher


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


def lab8_index(request):
    tasks = [
        {
            "title": "Task 1",
            "description": "Books with price less than or equal to 80 using the Q operator.",
            "url_name": "lab8-task1",
        },
        {
            "title": "Task 2",
            "description": "Books with edition higher than 3 and title or author containing 'qu'.",
            "url_name": "lab8-task2",
        },
        {
            "title": "Task 3",
            "description": "Books with no edition higher than 3 and no 'qu' in title or author.",
            "url_name": "lab8-task3",
        },
        {
            "title": "Task 4",
            "description": "All books ordered by title using order_by.",
            "url_name": "lab8-task4",
        },
        {
            "title": "Task 5",
            "description": "Book count and price aggregates using Django aggregation functions.",
            "url_name": "lab8-task5",
        },
        {
            "title": "Task 7",
            "description": "Number of students in each city using the Address and Student models.",
            "url_name": "lab8-task7",
        },
    ]
    return render(request, "bookmodule/lab8_index.html", {"tasks": tasks})


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80)).order_by("id")
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        {
            "page_title": "Lab 8 - Task 1",
            "heading": "Books With Price Less Than or Equal to 80",
            "description": "Uses the Q operator to filter books whose price is less than or equal to 80.",
            "books": books,
        },
    )


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains="qu") | Q(author__icontains="qu"))
    ).order_by("id")
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        {
            "page_title": "Lab 8 - Task 2",
            "heading": "Books With Edition Greater Than 3 and 'qu' in Title or Author",
            "description": "Combines multiple Q expressions with & and | operators.",
            "books": books,
        },
    )


def lab8_task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) & ~Q(title__icontains="qu") & ~Q(author__icontains="qu")
    ).order_by("id")
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        {
            "page_title": "Lab 8 - Task 3",
            "heading": "Books With Edition Not Greater Than 3 and No 'qu' in Title or Author",
            "description": "Uses the ~ operator with Q expressions to build the opposite query.",
            "books": books,
        },
    )


def lab8_task4(request):
    books = Book.objects.order_by("title")
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        {
            "page_title": "Lab 8 - Task 4",
            "heading": "Books Ordered by Title",
            "description": "Lists all books ordered alphabetically by title using order_by.",
            "books": books,
        },
    )


def lab8_task5(request):
    stats = Book.objects.aggregate(
        total_books=Count("id"),
        total_price=Sum("price"),
        average_price=Avg("price"),
        maximum_price=Max("price"),
        minimum_price=Min("price"),
    )
    return render(
        request,
        "bookmodule/lab8_aggregation.html",
        {
            "page_title": "Lab 8 - Task 5",
            "stats": stats,
        },
    )


def lab8_task7(request):
    city_counts = Address.objects.annotate(student_count=Count("students")).order_by("city")
    return render(
        request,
        "bookmodule/lab8_city_counts.html",
        {
            "page_title": "Lab 8 - Task 7",
            "city_counts": city_counts,
        },
    )


def lab9_index(request):
    tasks = [
        {
            "title": "Task 1",
            "description": "List books with a transient percentage availability field.",
            "url_name": "lab9-task1",
        },
        {
            "title": "Task 2",
            "description": "List publishers annotated with their total book stock.",
            "url_name": "lab9-task2",
        },
        {
            "title": "Task 3",
            "description": "Get the oldest book managed by each publisher.",
            "url_name": "lab9-task3",
        },
        {
            "title": "Task 4",
            "description": "Calculate average, minimum, and maximum book prices per publisher.",
            "url_name": "lab9-task4",
        },
        {
            "title": "Task 5",
            "description": "Count highly rated books per publisher with their total quantity.",
            "url_name": "lab9-task5",
        },
        {
            "title": "Task 6",
            "description": "Count books per publisher filtered by price and quantity constraints.",
            "url_name": "lab9-task6",
        },
    ]
    return render(request, "bookmodule/lab9_index.html", {"tasks": tasks})


def lab9_task1(request):
    books = list(Book.objects.select_related("publisher").all().order_by("title"))
    total_quantity = sum(book.quantity for book in books)

    for book in books:
        if total_quantity:
            book.availability_percentage = (book.quantity / total_quantity) * 100
        else:
            book.availability_percentage = 0

    return render(
        request,
        "bookmodule/lab9_availability.html",
        {
            "page_title": "Lab 9 - Task 1",
            "books": books,
            "total_quantity": total_quantity,
        },
    )


def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_book_stock=Coalesce(Sum("books__quantity"), Value(0))
    ).order_by("name")
    rows = [
        [publisher.name, publisher.location, publisher.total_book_stock]
        for publisher in publishers
    ]
    return render(
        request,
        "bookmodule/lab9_publishers.html",
        {
            "page_title": "Lab 9 - Task 2",
            "heading": "Publishers With Total Book Stock",
            "headers": ["Name", "Location", "Total Book Stock"],
            "rows": rows,
        },
    )


def lab9_task3(request):
    oldest_books = Book.objects.filter(publisher=OuterRef("pk")).order_by("pubdate", "title")
    publishers = Publisher.objects.annotate(
        oldest_book_title=Subquery(oldest_books.values("title")[:1]),
        oldest_book_pubdate=Subquery(oldest_books.values("pubdate")[:1]),
    ).order_by("name")
    return render(
        request,
        "bookmodule/lab9_oldest_books.html",
        {
            "page_title": "Lab 9 - Task 3",
            "publishers": publishers,
        },
    )


def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        average_price=Avg("books__price"),
        minimum_price=Min("books__price"),
        maximum_price=Max("books__price"),
    ).order_by("name")
    rows = [
        [
            publisher.name,
            f"{publisher.average_price:.2f}" if publisher.average_price is not None else "0.00",
            f"{publisher.minimum_price:.2f}" if publisher.minimum_price is not None else "0.00",
            f"{publisher.maximum_price:.2f}" if publisher.maximum_price is not None else "0.00",
        ]
        for publisher in publishers
    ]
    return render(
        request,
        "bookmodule/lab9_publishers.html",
        {
            "page_title": "Lab 9 - Task 4",
            "heading": "Publisher Price Statistics",
            "headers": ["Name", "Average Price", "Minimum Price", "Maximum Price"],
            "rows": rows,
        },
    )


def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_books_count=Count("books", filter=Q(books__rating__gte=4), distinct=True),
        highly_rated_books_quantity=Coalesce(
            Sum("books__quantity", filter=Q(books__rating__gte=4)),
            Value(0),
        ),
    ).order_by("name")
    rows = [
        [
            publisher.name,
            publisher.highly_rated_books_count,
            publisher.highly_rated_books_quantity,
        ]
        for publisher in publishers
    ]
    return render(
        request,
        "bookmodule/lab9_publishers.html",
        {
            "page_title": "Lab 9 - Task 5",
            "heading": "Publishers With Highly Rated Books",
            "headers": ["Name", "Highly Rated Book Count", "Highly Rated Book Quantity"],
            "rows": rows,
        },
    )


def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_books_count=Count(
            "books",
            filter=Q(books__price__gt=50, books__quantity__lt=5, books__quantity__gte=1),
            distinct=True,
        )
    ).order_by("name")
    rows = [
        [publisher.name, publisher.filtered_books_count]
        for publisher in publishers
    ]
    return render(
        request,
        "bookmodule/lab9_publishers.html",
        {
            "page_title": "Lab 9 - Task 6",
            "heading": "Filtered Book Counts Per Publisher",
            "headers": ["Name", "Filtered Book Count"],
            "rows": rows,
        },
    )
