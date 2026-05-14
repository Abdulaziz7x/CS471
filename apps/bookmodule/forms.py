from django import forms

from .models import Address2, Book, GalleryItem, Student, Student2


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "price", "edition"]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_edition(self):
        edition = self.cleaned_data["edition"]
        if edition < 1:
            raise forms.ValidationError("Edition must be at least 1.")
        return edition


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "age", "address"]


class Student2Form(forms.ModelForm):
    addresses = forms.ModelMultipleChoiceField(
        queryset=Address2.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Student2
        fields = ["name", "age", "addresses"]


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ["title", "description", "image"]
