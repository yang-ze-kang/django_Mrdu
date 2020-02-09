#!/usr/bin/env python
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="邮箱", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    code = forms.EmailField(label="验证码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','password','email']
    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     user
    #     if commit:
    #         user.save()
    #     return user

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ['password']
#     def clean_password(self):
#         # always return the initial value
#         return self.initial['password']

class UserInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['last_name','first_name','username','password','is_active','is_staff','is_superuser','user_permissions','last_login','date_joined','groups']

class ImageForm(forms.Form):
    img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
