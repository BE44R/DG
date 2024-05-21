"""This module describes forms"""
from django import forms
from django.contrib.auth.models import User


class SendMessageFrom(forms.Form):
    """This is send message form"""
    text = forms.CharField(max_length=500, required=False)
    chat_id = forms.IntegerField()
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def clean(self):
        text = self.cleaned_data.get('text')
        chat_id = self.cleaned_data.get('chat_id')
        files = self.cleaned_data.get('files')
        if not text and not files:
            raise forms.ValidationError('Empty message')
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    """This is change password form"""
    old_password = forms.CharField(max_length=500)
    new_password = forms.CharField(max_length=500)


class CreateChatForm(forms.Form):
    """This is create chat form"""
    user_to = forms.CharField(max_length=1000, label='')


class UserRegistrationForm(forms.ModelForm):
    """This is user registrations form"""
    """This class provide you an opportunity to register on the site
        fields:
        password - password to your account
        password2 - repeat the password
        methods:
        clean_password2 - function that clean the field? if the passwords didn`t match
    """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        """This class adds you a username"""
        model = User
        fields = ('username',)

    def clean_password2(self):
        """This function cleans your password"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class GlobalChatForm(forms.Form):
    """This is send message form"""
    text = forms.CharField(max_length=1000, required=False, label='')
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, label='')


class Buy(forms.Form):
    """This is buy form"""
    key = forms.CharField(max_length=100)
