from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from app.forms import BookForm
from app.services.book_service import BookService
from app.services.borrowing_service import BorrowingService


def book_detail(request, book_id):
    book = BookService.get_detail(book_id)

    if book is None:
        raise Http404("Book not found.")

    status = BorrowingService.get_book_status(book, request.user)

    return render(request, "pages/book_detail.html", {
        "book": book,
        **status,
    })


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = BookService.create(owner=request.user, **form.cleaned_data)
            messages.success(request, f'"{book.title}" was added to the shelf.')

            return redirect("book-detail", book_id=book.id)
    else:
        form = BookForm()

    return render(request, "pages/book_form.html", {
        "form": form,
        "mode": "create",
    })


@login_required
def book_update(request, book_id):
    book = BookService.get_detail(book_id)

    if book is None:
        raise Http404("Book not found.")

    if not BookService.is_owner(book, request.user):
        return HttpResponseForbidden("You can only edit books you own.")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            BookService.update(book.id, **form.cleaned_data)
            messages.success(request, f'"{book.title}" was updated.')

            return redirect("book-detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, "pages/book_form.html", {
        "form": form,
        "mode": "update",
        "book": book,
    })


@login_required
def book_delete(request, book_id):
    book = BookService.get_detail(book_id)

    if book is None:
        raise Http404("Book not found.")

    if not BookService.is_owner(book, request.user):
        return HttpResponseForbidden("You can only delete books you own.")

    if request.method == "POST":
        title = book.title
        BookService.delete(book.id)
        messages.success(request, f'"{title}" was removed from the shelf.')

        return redirect("home")

    return redirect("book-detail", book_id=book.id)
