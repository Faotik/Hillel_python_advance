from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("books", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book"),
    path("authors", views.AuthorsListView.as_view(), name="authors"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author"),
    path("author/edit/<int:pk>", views.editAuthorView, name="edit-author-form"),
    path("author/add", views.addAuthorView, name="add-author-form"),
    path("author/delete/<int:pk>", views.deleteAuthorView, name="delete-author"),
    path("book/delete/<int:pk>", views.deleteBookView, name="delete-book"),
]
