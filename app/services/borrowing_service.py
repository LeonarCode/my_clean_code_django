from django.db import transaction

from app.repositories.book_repository import BookRepository
from app.repositories.borrowing_repository import BorrowingRepository
from app.services.book_service import BookService


class BorrowingService:
    @staticmethod
    @transaction.atomic
    def borrow_book(user, book_id):

        book = BookRepository.get_by_id(book_id)

        if not book:
            raise ValueError("Book does not exist.")

        if not book.available:
            raise ValueError("Book is not available.")

        borrowing = BorrowingRepository.create(
            user=user,
            book=book,
        )

        BookRepository.update(
            book.id,
            available=False,
        )

        return borrowing

    @staticmethod
    @transaction.atomic
    def return_book(borrowing_id):

        borrowing = BorrowingRepository.get_by_id(
            borrowing_id
        )

        if not borrowing:
            raise ValueError("Borrowing not found.")

        if borrowing.status != "borrowed":
            raise ValueError("Borrowing is not active.")

        borrowing = BorrowingRepository.mark_as_returned(
            borrowing
        )

        BookRepository.update(
            borrowing.book.id,
            available=True,
        )

        return borrowing

    @staticmethod
    def get_borrowing(borrowing_id):
        return BorrowingRepository.get_by_id(borrowing_id)

    @staticmethod
    def is_borrower(borrowing, user):
        return bool(borrowing and user.is_authenticated and borrowing.user_id == user.id)

    @staticmethod
    def get_borrow_state(book, user):
        """Whether `book` is currently borrowed by `user`, and by whom if not."""
        active_borrowing = BorrowingRepository.get_active_by_book(book)
        is_borrowed_by_me = bool(
            active_borrowing
            and user.is_authenticated
            and active_borrowing.user_id == user.id
        )

        return {
            "active_borrowing": active_borrowing,
            "is_borrowed_by_me": is_borrowed_by_me,
        }

    @staticmethod
    def get_book_status(book, user):
        """Everything a book detail/status/card template needs to decide
        which action (borrow / return / manage / unavailable) to show.
        """
        status = BorrowingService.get_borrow_state(book, user)
        status["is_owner"] = BookService.is_owner(book, user)

        return status

    @staticmethod
    def annotate_catalog(books, user):
        """Attach is_owner / is_borrowed_by_me / active_borrowing to each book
        in a list, using a single query for the user's active borrowings
        instead of one per book.
        """
        active_by_book = {}
        if user.is_authenticated:
            active_by_book = {
                borrowing.book_id: borrowing
                for borrowing in BorrowingRepository.get_active_by_user(user)
            }

        for book in books:
            book.is_owner = BookService.is_owner(book, user)
            book.active_borrowing = active_by_book.get(book.id)
            book.is_borrowed_by_me = book.active_borrowing is not None

        return books

    @staticmethod
    def get_my_borrowings(user):
        return {
            "active_borrowings": BorrowingRepository.get_active_by_user(user),
            "history": BorrowingRepository.get_history_by_user(user),
        }
