from django import forms
from .models import *


class SearchForm(forms.Form):
    search = forms.CharField(max_length=10000, widget=forms.Textarea)


# class ProductCommentForm(forms.ModelForm):
#     class Meta:
#         model = ProductCommentModel
#         fields = ['user', 'product', 'text', 'grade']