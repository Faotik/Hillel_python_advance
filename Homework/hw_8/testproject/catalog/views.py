from django import views
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from .forms import EditAuthorForm, AddAuthorForm
from typing import Any
from django.http import HttpResponseRedirect
from django.urls import path
from django.urls import reverse

# Create your views here.


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    queryset = Book.objects.all()
    template_name = "book/list.html"

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     return super().get_context_data(**kwargs) | {"book_list": Book.objects.all()}


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book/detail.html"


class AuthorsListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    queryset = Author.objects.all()
    template_name = "author/list.html"


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.all().count()

    return render(
        request,
        "index.html",
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
        },
    )


def addAuthorView(request):

    if request.method == "POST":
        form = AddAuthorForm(request.POST)

        if form.is_valid():
            author = Author.objects.create()
            (author.name, author.date_of_birth, author.date_of_death) = form.clean_data()
            author.save()

            return HttpResponseRedirect("/")
    else:
        form = AddAuthorForm()

    return render(request, "author/addAuthor.html",
        {
            "form": form,
        }
    )


def editAuthorView(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == "POST":
        form = EditAuthorForm(request.POST)

        if form.is_valid():

            (author.name, author.date_of_birth, author.date_of_death) = form.clean_data()
            author.save()

            return HttpResponseRedirect("/")
    else:
        form = EditAuthorForm(initial={
                            "name": author.name,
                            "date_of_birth": author.date_of_birth,
                            "date_of_death": author.date_of_death})

    return render(request, "author/editAuthor.html",
        {
            "author": author,
            "form": form,
        }
    )


def deleteAuthorView(request, pk):
    author = get_object_or_404(Author, pk=pk)

    author.delete()

    return redirect(reverse('authors'))


def deleteBookView(request, pk):
    book = get_object_or_404(Book, pk=pk)

    book.delete()

    return redirect(reverse('books'))
