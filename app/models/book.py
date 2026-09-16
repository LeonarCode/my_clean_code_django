from django.db import models
from .category import Category
from django.contrib.auth.models import User


class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='book_images/', blank=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"