from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError


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
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        widgets = {
            'username':forms.TextInput(attrs={'placeholder':'กรอกชื่อผู้ใช้','class':''}),
            'first_name':forms.TextInput(attrs={'placeholder':'ชื่อจริง','class':'','required':True}),
            'last_name':forms.TextInput(attrs={'placeholder':'นามสกุล','class':'','required':True}),
            'email':forms.EmailInput(attrs={'placeholder':'อีเมล','class':'','required':True}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("อีเมลนี้มีผู้ใช้งานแล้ว")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number']
        labels = {
            'address': 'ที่อยู่',
            'phone_number': 'เบอร์โทร',
        }

        widgets = {
            'phone_number':forms.TextInput(attrs={'placeholder':'กรอกเบอร์โทร','class':''}),

            'address':forms.Textarea(attrs={'placeholder':'กรอกที่อยู่','class':'h-24 '}),
            'phone_number':forms.TextInput(attrs={'placeholder':'กรอกเบอร์โทร','class':''}),
        }

class ChangePasswordForm(PasswordChangeForm):
    pass


class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
