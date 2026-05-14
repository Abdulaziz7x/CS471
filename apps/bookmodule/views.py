from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Min, OuterRef, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, GalleryItemForm, Student2Form, StudentForm
from .models import Address, Address2, Book, GalleryItem, Publisher, Student, Student2


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


def lab10_index(request):
    sections = [
        {
            "title": "Part 1",
            "description": "CRUD operations using direct Django model handling.",
            "links": [
                {"label": "List Books", "url_name": "lab10-part1-list"},
                {"label": "Add Book", "url_name": "lab10-part1-add"},
            ],
        },
        {
            "title": "Part 2",
            "description": "CRUD operations reimplemented using Django forms validation.",
            "links": [
                {"label": "List Books", "url_name": "lab10-part2-list"},
                {"label": "Add Book", "url_name": "lab10-part2-add"},
            ],
        },
    ]
    return render(request, "bookmodule/lab10_index.html", {"sections": sections})


def lab10_part1_list_books(request):
    books = Book.objects.order_by("title", "id")
    return render(
        request,
        "bookmodule/lab10_book_list.html",
        {
            "page_title": "Lab 10 - Part 1",
            "heading": "Lab 10 Part 1: CRUD Operations",
            "description": "List, add, edit, and delete books using direct model operations.",
            "books": books,
            "add_url_name": "lab10-part1-add",
            "edit_url_name": "lab10-part1-edit",
            "delete_url_name": "lab10-part1-delete",
        },
    )


def _manual_book_payload(request):
    title = request.POST.get("title", "").strip()
    author = request.POST.get("author", "").strip()
    price = request.POST.get("price", "").strip()
    edition = request.POST.get("edition", "").strip()

    errors = {}
    if not title:
        errors["title"] = "Title is required."
    if not author:
        errors["author"] = "Author is required."

    try:
        price_value = float(price)
        if price_value <= 0:
            errors["price"] = "Price must be greater than zero."
    except ValueError:
        errors["price"] = "Price must be a valid number."
        price_value = 0.0

    try:
        edition_value = int(edition)
        if edition_value < 1:
            errors["edition"] = "Edition must be at least 1."
    except ValueError:
        errors["edition"] = "Edition must be a whole number."
        edition_value = 1

    return {
        "title": title,
        "author": author,
        "price": price,
        "edition": edition,
    }, errors, price_value, edition_value


def lab10_part1_add_book(request):
    initial = {"title": "", "author": "", "price": "0.0", "edition": "1"}
    errors = {}

    if request.method == "POST":
        initial, errors, price_value, edition_value = _manual_book_payload(request)
        if not errors:
            Book.objects.create(
                title=initial["title"],
                author=initial["author"],
                price=price_value,
                edition=edition_value,
            )
            return redirect("lab10-part1-list")

    return render(
        request,
        "bookmodule/lab10_book_form_manual.html",
        {
            "page_title": "Lab 10 - Part 1 Add Book",
            "heading": "Add Book (Part 1)",
            "description": "Creates a new book using direct Django model operations.",
            "values": initial,
            "errors": errors,
            "submit_label": "Create Book",
            "cancel_url_name": "lab10-part1-list",
        },
    )


def lab10_part1_edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    initial = {
        "title": book.title,
        "author": book.author,
        "price": str(book.price),
        "edition": str(book.edition),
    }
    errors = {}

    if request.method == "POST":
        initial, errors, price_value, edition_value = _manual_book_payload(request)
        if not errors:
            book.title = initial["title"]
            book.author = initial["author"]
            book.price = price_value
            book.edition = edition_value
            book.save()
            return redirect("lab10-part1-list")

    return render(
        request,
        "bookmodule/lab10_book_form_manual.html",
        {
            "page_title": "Lab 10 - Part 1 Edit Book",
            "heading": f"Edit Book (Part 1): {book.title}",
            "description": "Updates the selected book using direct Django model operations.",
            "values": initial,
            "errors": errors,
            "submit_label": "Update Book",
            "cancel_url_name": "lab10-part1-list",
        },
    )


def lab10_part1_delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect("lab10-part1-list")


def lab10_part2_list_books(request):
    books = Book.objects.order_by("title", "id")
    return render(
        request,
        "bookmodule/lab10_book_list.html",
        {
            "page_title": "Lab 10 - Part 2",
            "heading": "Lab 10 Part 2: CRUD With Validation",
            "description": "List, add, edit, and delete books using Django forms validation.",
            "books": books,
            "add_url_name": "lab10-part2-add",
            "edit_url_name": "lab10-part2-edit",
            "delete_url_name": "lab10-part2-delete",
        },
    )


def lab10_part2_add_book(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab10-part2-list")

    return render(
        request,
        "bookmodule/lab10_book_form_validated.html",
        {
            "page_title": "Lab 10 - Part 2 Add Book",
            "heading": "Add Book (Part 2)",
            "description": "Creates a new book using a Django form with validation.",
            "form": form,
            "submit_label": "Create Book",
            "cancel_url_name": "lab10-part2-list",
        },
    )


def lab10_part2_edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab10-part2-list")

    return render(
        request,
        "bookmodule/lab10_book_form_validated.html",
        {
            "page_title": "Lab 10 - Part 2 Edit Book",
            "heading": f"Edit Book (Part 2): {book.title}",
            "description": "Updates the selected book using a Django form with validation.",
            "form": form,
            "submit_label": "Update Book",
            "cancel_url_name": "lab10-part2-list",
        },
    )


def lab10_part2_delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect("lab10-part2-list")


@login_required
def lab11_index(request):
    tasks = [
        {
            "title": "Task 1",
            "description": "CRUD students with a single Address using Django form fields.",
            "url_name": "lab11-task1-list",
        },
        {
            "title": "Task 2",
            "description": "CRUD students with multiple addresses using a many-to-many relationship.",
            "url_name": "lab11-task2-list",
        },
        {
            "title": "Task 3",
            "description": "Manage a custom image/file table using Django forms and upload handling.",
            "url_name": "lab11-task3-list",
        },
    ]
    return render(request, "bookmodule/lab11_index.html", {"tasks": tasks})


@login_required
def lab11_task1_list_students(request):
    students = Student.objects.select_related("address").order_by("name", "id")
    return render(
        request,
        "bookmodule/lab11_students_list.html",
        {
            "page_title": "Lab 11 - Task 1",
            "heading": "Lab 11 Task 1: Students and One Address",
            "description": "List, add, edit, and delete students with one address per student.",
            "students": students,
            "add_url_name": "lab11-task1-add",
            "edit_url_name": "lab11-task1-edit",
            "delete_url_name": "lab11-task1-delete",
            "many_to_many": False,
        },
    )


@login_required
def lab11_task1_add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab11-task1-list")
    return render(
        request,
        "bookmodule/lab11_student_form.html",
        {
            "page_title": "Lab 11 - Add Student",
            "heading": "Add Student (One Address)",
            "description": "Create a student and assign one address using a Django form field.",
            "form": form,
            "submit_label": "Create Student",
            "cancel_url_name": "lab11-task1-list",
        },
    )


@login_required
def lab11_task1_edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab11-task1-list")
    return render(
        request,
        "bookmodule/lab11_student_form.html",
        {
            "page_title": "Lab 11 - Edit Student",
            "heading": f"Edit Student: {student.name}",
            "description": "Update the student and its single address.",
            "form": form,
            "submit_label": "Update Student",
            "cancel_url_name": "lab11-task1-list",
        },
    )


@login_required
def lab11_task1_delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect("lab11-task1-list")


@login_required
def lab11_task2_list_students(request):
    students = Student2.objects.prefetch_related("addresses").order_by("name", "id")
    return render(
        request,
        "bookmodule/lab11_students_list.html",
        {
            "page_title": "Lab 11 - Task 2",
            "heading": "Lab 11 Task 2: Students and Multiple Addresses",
            "description": "List, add, edit, and delete students in a many-to-many relationship.",
            "students": students,
            "add_url_name": "lab11-task2-add",
            "edit_url_name": "lab11-task2-edit",
            "delete_url_name": "lab11-task2-delete",
            "many_to_many": True,
        },
    )


@login_required
def lab11_task2_add_student(request):
    form = Student2Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab11-task2-list")
    return render(
        request,
        "bookmodule/lab11_student_form.html",
        {
            "page_title": "Lab 11 - Add Student2",
            "heading": "Add Student (Multiple Addresses)",
            "description": "Create a student and assign multiple addresses using a many-to-many field.",
            "form": form,
            "submit_label": "Create Student",
            "cancel_url_name": "lab11-task2-list",
        },
    )


@login_required
def lab11_task2_edit_student(request, student_id):
    student = get_object_or_404(Student2, pk=student_id)
    form = Student2Form(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab11-task2-list")
    return render(
        request,
        "bookmodule/lab11_student_form.html",
        {
            "page_title": "Lab 11 - Edit Student2",
            "heading": f"Edit Student: {student.name}",
            "description": "Update the student and its address selections.",
            "form": form,
            "submit_label": "Update Student",
            "cancel_url_name": "lab11-task2-list",
        },
    )


@login_required
def lab11_task2_delete_student(request, student_id):
    student = get_object_or_404(Student2, pk=student_id)
    student.delete()
    return redirect("lab11-task2-list")


@login_required
def lab11_task3_list_gallery(request):
    items = GalleryItem.objects.order_by("title", "id")
    return render(
        request,
        "bookmodule/lab11_gallery_list.html",
        {
            "page_title": "Lab 11 - Task 3",
            "heading": "Lab 11 Task 3: File/Image Handling",
            "description": "Manage a custom gallery-style table with uploaded image files.",
            "items": items,
        },
    )


@login_required
def lab11_task3_add_gallery_item(request):
    form = GalleryItemForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab11-task3-list")
    return render(
        request,
        "bookmodule/lab11_gallery_form.html",
        {
            "page_title": "Lab 11 - Add Gallery Item",
            "heading": "Add Gallery Item",
            "description": "Upload an image file through Django form handling.",
            "form": form,
            "submit_label": "Create Item",
            "cancel_url_name": "lab11-task3-list",
        },
    )
