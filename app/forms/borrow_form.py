from django import forms


class BorrowForm(forms.Form):
    book_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )