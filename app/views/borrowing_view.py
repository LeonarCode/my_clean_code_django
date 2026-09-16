from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render

from app.services.book_service import BookService
from app.services.borrowing_service import BorrowingService


def _borrow_panel_response(request, book):
    """Render the fragment htmx should swap in after a borrow/return action."""
    if not request.htmx:
        return redirect(request.POST.get("next") or "home")

    status = BorrowingService.get_book_status(book, request.user)
    context = {"book": book, **status}

    panel = request.GET.get("panel")
    if panel == "detail":
        template = "partials/book_status_swap.html"
    elif panel == "list":
        # Row-based views (e.g. "my borrowings") just want the row gone plus a toast,
        # not a re-rendered book card.
        template = "partials/toast_oob.html"
    else:
        template = "partials/book_card_swap.html"

    return render(request, template, context)


@login_required
def borrow_book(request, book_id):
    book = BookService.get_detail(book_id)

    if book is None:
        raise Http404("Book not found.")

    if request.method == "POST":
        try:
            BorrowingService.borrow_book(request.user, book_id)
            messages.success(request, f'You borrowed "{book.title}". Enjoy the read!')
        except ValueError as exc:
            messages.error(request, str(exc))
        book = BookService.get_detail(book_id)

    return _borrow_panel_response(request, book)


@login_required
def return_book(request, borrowing_id):
    borrowing = BorrowingService.get_borrowing(borrowing_id)

    if borrowing is None:
        messages.error(request, "Borrowing not found.")
        return redirect("my-borrowings")

    if not BorrowingService.is_borrower(borrowing, request.user):
        return HttpResponseForbidden("You can only return books you borrowed.")

    book = borrowing.book

    if request.method == "POST":
        try:
            BorrowingService.return_book(borrowing_id)
            messages.success(request, f'You returned "{book.title}".')
        except ValueError as exc:
            messages.error(request, str(exc))
        book = BookService.get_detail(book.id)

    return _borrow_panel_response(request, book)


@login_required
def my_borrowings(request):
    context = BorrowingService.get_my_borrowings(request.user)
    return render(request, "pages/my_borrowings.html", context)
