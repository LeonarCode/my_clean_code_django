from django.urls import path

from app.views import book_view, borrowing_view, home_views

urlpatterns = [
    path('', home_views.home, name='home'),

    path('books/create/', book_view.book_create, name='book-create'),
    path('books/<int:book_id>/', book_view.book_detail, name='book-detail'),
    path('books/<int:book_id>/edit/', book_view.book_update, name='book-update'),
    path('books/<int:book_id>/delete/', book_view.book_delete, name='book-delete'),

    path('books/<int:book_id>/borrow/', borrowing_view.borrow_book, name='book-borrow'),
    path('borrowings/', borrowing_view.my_borrowings, name='my-borrowings'),
    path('borrowings/<int:borrowing_id>/return/', borrowing_view.return_book, name='borrowing-return'),
]
