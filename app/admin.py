from django.contrib import admin

from app.models import Book, Borrowing, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "owner", "available"]
    list_filter = ["category", "available"]
    search_fields = ["title", "author", "isbn"]


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "status", "borrowed_at", "returned_at"]
    list_filter = ["status"]
