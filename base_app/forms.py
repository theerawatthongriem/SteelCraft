from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='ชื่อผู้ใช้',
        widget=forms.TextInput(attrs={'placeholder': 'กรอกชื่อผู้ใช้'}),
    )
    password = forms.CharField(
        label='รหัสผ่าน',
        widget=forms.PasswordInput(attrs={'placeholder': 'กรอกรหัสผ่าน',}),
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ChangePasswordForm(PasswordChangeForm):
    pass

