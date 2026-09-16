from django.utils import timezone

from app.models import Borrowing


class BorrowingRepository:
    @staticmethod
    def create(user, book):
        return Borrowing.objects.create(
            user=user,
            book=book,
            status="borrowed",
        )

    @staticmethod
    def get_by_id(borrowing_id):
        return Borrowing.objects.select_related(
            "book", "book__category", "book__owner", "user"
        ).filter(
            id=borrowing_id
        ).first()

    @staticmethod
    def get_active_by_user(user):
        return Borrowing.objects.filter(
            user=user,
            status="borrowed",
        ).select_related("book", "book__category")

    @staticmethod
    def get_active_by_book(book):
        return Borrowing.objects.filter(
            book=book,
            status="borrowed",
        ).first()

    @staticmethod
    def get_history_by_user(user):
        return Borrowing.objects.filter(
            user=user,
            status="returned",
        ).select_related("book", "book__category").order_by("-returned_at")

    @staticmethod
    def mark_as_returned(borrowing):
        borrowing.status = "returned"
        borrowing.returned_at = timezone.now()
        borrowing.save(
            update_fields=["status", "returned_at"]
        )

        return borrowing