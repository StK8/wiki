from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new_entry, name="new_entry"),
    path("random", views.random, name="random_entry"),
    path("<str:entry_name>/edit", views.edit, name="edit"),
    path("<str:entry_name>", views.entry, name="entry")
]
