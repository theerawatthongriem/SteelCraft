from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address','phone_number']

        labels = {
            'address':'ที่อยู่',
            'phone_number':'เบอร์โทร',
        }

class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ChangePasswordForm(PasswordChangeForm):
    pass

