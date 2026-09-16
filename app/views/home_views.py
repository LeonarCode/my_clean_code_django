from django.shortcuts import render

from app.services.book_service import BookService
from app.services.borrowing_service import BorrowingService
from app.services.category_service import CategoryService


def home(request):
    catalog = BookService.get_catalog_page(
        query=request.GET.get("q", ""),
        category_id=request.GET.get("category", ""),
        page_number=request.GET.get("page"),
    )
    BorrowingService.annotate_catalog(catalog["books"], request.user)

    context = {
        "page_obj": catalog["page_obj"],
        "books": catalog["books"],
        "categories": CategoryService.get_all(),
        "query": catalog["query"],
        "selected_category": catalog["category_id"],
    }

    template = "partials/book_grid.html" if request.htmx else "pages/homepage.html"
    return render(request, template, context)
