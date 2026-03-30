from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="book-index"),
    path("index2/<int:val1>/", views.index2, name="book-index2"),
    path("html5/links", views.lab5_links, name="lab5-links"),
    path("html5/formatting", views.lab5_formatting, name="lab5-formatting"),
    path("html5/listing", views.lab5_listing, name="lab5-listing"),
    path("html5/tables", views.lab5_tables, name="lab5-tables"),
    path("<int:bookId>", views.viewbook, name="view-book"),
]
