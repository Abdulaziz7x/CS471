# CS471

Course repository for CS471 Web Technologies.

This project contains Django-based lab work and examples for topics such as routing, templates, forms, models, queries, and multi-model relationships.

## Project Structure

- `apps/bookmodule/` contains the book-related views, models, URLs, migrations, and tests
- `apps/usermodule/` contains the user form example
- `apps/templates/` contains shared and app-specific templates
- `DjangoProjects/` contains the main Django project settings and URL configuration

## Running The Project

1. Create a virtual environment:
   `python3 -m venv .venv`
2. Activate it:
   `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Apply migrations:
   `python3 manage.py migrate`
5. Start the development server:
   `python3 manage.py runserver`

## Testing

Run the test suite with:

`python3 manage.py test`
