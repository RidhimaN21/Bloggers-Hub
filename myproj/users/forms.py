from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import UserProfile
from django.utils.translation import gettext_lazy as _

class CustomForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','email','password1','password2']
        labels = {
            'Username': _('username'),
            'First Name': _('first_name'),
            'email': _('email'),
            'password1': _('password1'),
            'password2': _('password2'),
        }
        help_texts = {
            'username' : None,
        }

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','email']
        labels = {
            'username': _('username'),
            'first_name': _('first_name'),
            'email': _('email'),
        }
        help_texts = {
            'username' : None,
        }
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['alternate_email']
        labels = {
            'alternate_email': _('alternate_email'),
        }


class BackupOrPasswordLoginForm(forms.Form):
    LOGIN_CHOICES = (
        ('password', 'Password'),
        ('token', 'Token'),
    )
    login_method = forms.ChoiceField(choices=LOGIN_CHOICES, widget=forms.RadioSelect, initial='password')
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    token = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned = super().clean()
        login_method = cleaned.get('login_method')
        password = cleaned.get('password')
        token = cleaned.get('token')
        if login_method == 'password' and not password:
            self.add_error('password', 'Password is required for password login.')
        if login_method == 'token' and not token:
            self.add_error('token', 'Token is required for token login.')
        return cleaned











# class BackupOrPasswordLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput,required=False)
#     token = forms.CharField( required=False)

#     def clean(self):
#         cleaned = super().clean()
#         if not cleaned.get('password') and cleaned.get('token'):
#             raise forms.ValidationError("Enter passowrd or token to login .")
#         return cleaned












