from django import forms

from app.forms.styles import FILE_CLASSES, INPUT_CLASSES, SELECT_CLASSES
from app.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "category",
            "title",
            "image",
            "author",
            "isbn",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": SELECT_CLASSES}),
            "title": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "e.g. Introduction to Algorithms",
                "autofocus": True,
            }),
            "image": forms.ClearableFileInput(attrs={"class": FILE_CLASSES}),
            "author": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "e.g. Thomas H. Cormen",
            }),
            "isbn": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "e.g. 978-0262046305",
            }),
        }
        labels = {
            "isbn": "ISBN",
        }
