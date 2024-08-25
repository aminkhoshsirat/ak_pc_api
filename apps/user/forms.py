from django import forms
from .models import *
from django.core.validators import MinLengthValidator


class UserLoginForm(forms.Form):
    phone_or_email = forms.CharField(max_length=300)
    password = forms.CharField(max_length=25)


class UserRegisterActivationForm(forms.Form):
    code = forms.CharField(max_length=6)
    phone = forms.CharField(max_length=11)
    fullname = forms.CharField(max_length=1000)
    email = forms.EmailField()
    password = forms.CharField(max_length=25)
    confirm_password = forms.CharField(max_length=25)

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if confirm_password == password:
            if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
                raise forms.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد و حداقل 8 کاراکتر.')
            else:
                return confirm_password
        else:
            raise forms.ValidationError('پسورد و تکرار آن یکی نمی باشد')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['fullname', 'email', 'post_code', 'address', 'profile_image']


class UserChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=25)
    confirm_password = forms.CharField(max_length=25)

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if confirm_password == password:
            if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
                raise forms.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد و حداقل 8 کاراکتر.')
            else:
                return confirm_password
        else:
            raise forms.ValidationError('پسورد و تکرار آن یکی نمی باشد')


class NeshanSearchForm(forms.Form):
    search = forms.CharField(widget=forms.Textarea(), max_length=10000)


class NeshanPositionForm(forms.Form):
    x = forms.CharField(max_length=100)
    y = forms.CharField(max_length=100)


class AddressForm(forms.Form):
    state = forms.CharField(max_length=10000)
    city = forms.CharField(max_length=10000)
    address = forms.CharField(widget=forms.Textarea())
    plaque = forms.CharField(max_length=1000)
    post_code = forms.CharField(max_length=10)
    position_x = forms.FloatField()
    position_y = forms.FloatField()

    def clean_plaque(self):
        plaque = self.cleaned_data['plaque']
        if plaque.isdigit():
            return plaque
        else:
            return forms.ValidationError('پلاک باید عدد باشد')

    def clean_post_code(self):
        post_code = self.cleaned_data['post_code']
        if post_code.isdigit() and len(post_code) == 10:
            return post_code
        else:
            return forms.ValidationError('کد پستی باید ده رقم باشد')


class SendOtpForm(forms.Form):
    phone = forms.CharField(max_length=11)


class AddAdminForm(forms.ModelForm):
    class Meta:
        model = UserModel
        exclude = ['ban']

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
            raise forms.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد و حداقل 8 کاراکتر.')
        else:
            return password


class AddUserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        exclude = ['ban', 'groups', 'is_staff', 'is_superuser', 'user_permissions', 'is_staff', 'designation', 'is_admin']

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
            raise forms.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد و حداقل 8 کاراکتر.')
        else:
            return password
