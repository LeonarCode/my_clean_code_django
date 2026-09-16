from django.core.paginator import Paginator

from app.repositories.book_repository import BookRepository

CATALOG_PAGE_SIZE = 8


class BookService:
    @staticmethod
    def create(**data):
        return BookRepository.create(**data)

    @staticmethod
    def get_all():
        return BookRepository.get_all()

    @staticmethod
    def get_by_id(book_id):
        return BookRepository.get_by_id(book_id)

    @staticmethod
    def get_detail(book_id):
        return BookRepository.get_detail_by_id(book_id)

    @staticmethod
    def update(book_id, **data):
        return BookRepository.update(book_id, **data)

    @staticmethod
    def delete(book_id):
        return BookRepository.delete(book_id)

    @staticmethod
    def is_owner(book, user):
        return bool(book and user.is_authenticated and book.owner_id == user.id)

    @staticmethod
    def get_catalog_page(query, category_id, page_number, per_page=CATALOG_PAGE_SIZE):
        """Search/filter/paginate the book catalog. Returns everything the
        home view needs to build its context, with input already normalized.
        """
        query = (query or "").strip()
        category_id = category_id if (category_id or "").strip().isdigit() else ""

        books = BookRepository.find_catalog(query=query, category_id=category_id)

        paginator = Paginator(books, per_page)
        page_obj = paginator.get_page(page_number)

        return {
            "page_obj": page_obj,
            "books": list(page_obj.object_list),
            "query": query,
            "category_id": category_id,
        }
