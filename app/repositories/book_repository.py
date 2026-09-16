from django.db.models import Q

from app.models import Book


class BookRepository:
    @staticmethod
    def create(**data):
        return Book.objects.create(**data)

    @staticmethod
    def get_all():
        return Book.objects.all()

    @staticmethod
    def get_by_id(book_id):
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def get_detail_by_id(book_id):
        return Book.objects.select_related("category", "owner").filter(id=book_id).first()

    @staticmethod
    def update(book_id, **data):
        book = Book.objects.filter(id=book_id).first()

        if not book:
            return None

        for field, value in data.items():
            setattr(book, field, value)
        book.save()

        return book

    @staticmethod
    def delete(book_id):
        return Book.objects.filter(id=book_id).delete()

    @staticmethod
    def search(query):
        return Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    @staticmethod
    def find_catalog(query="", category_id=None):
        books = BookRepository.search(query) if query else Book.objects.all()

        if category_id:
            books = books.filter(category_id=category_id)

        return books.select_related("category", "owner").order_by("title")
