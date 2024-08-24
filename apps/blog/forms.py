from django import forms
from .models import *


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), required=True)
    replay_to = forms.IntegerField(required=False)


class AutherForm(forms.ModelForm):
    class Meta:
        model = AutherModel
        exclude = ['ban', 'groups', 'is_staff', 'is_superuser', 'user_permissions', 'is_staff', 'designation',
                   'is_admin']

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
            raise forms.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد و حداقل 8 کاراکتر.')
        else:
            return password


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = '__all__'


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategoryModel
        fields = '__all__'
