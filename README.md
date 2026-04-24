# CS471

Labs solutions for CS471 Web Technologies.

## Lab 5

This repo now includes Lab 5 for HTML and CSS (Part 2) using Django routes under:

- `/books/html5/links`
- `/books/html5/formatting`
- `/books/html5/listing`
- `/books/html5/tables`

## Lab 8

This repo also includes Lab 8 for Django Models (Part 2) under:

- `/books/lab8/task1`
- `/books/lab8/task2`
- `/books/lab8/task3`
- `/books/lab8/task4`
- `/books/lab8/task5`
- `/books/lab8/task7`

The implementation adds:

- a `Book` model with seeded fake data
- `Address` and `Student` models
- query pages using `Q`, sorting with `order_by`, and aggregation functions
- a grouped city summary showing the number of students in each city

## Run The Server

1. Create a virtual environment:
   `python3 -m venv .venv`
2. Activate it:
   `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the server:
   `python3 manage.py runserver`
