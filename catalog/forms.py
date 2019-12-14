from django import forms
from django.contrib.auth.models import User

from .models import Reviews


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ['comment', 'rating']

    def save(self, *args, **kwargs):

        user = kwargs.get('user')
        book = kwargs.get('book')

        comment = super().save(commit=False)

        comment.author = user
        comment.book = book

        comment.save()

        return comment


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ('username', 'password', 'password_check', 'first_name', 'last_name', 'email')
        help_texts = {
            'username': None,
        }

    def clean(self):

        cleaned_data = self.cleaned_data

        username = cleaned_data['username']
        password = cleaned_data['password']
        password_check = cleaned_data['password_check']
        email = cleaned_data['email']

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким именем уже зарегестрирован!')

        if password != password_check:
            self.add_error('password', 'Пароли не совпадают!')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Пользователь с таким емайлом уже зарегестрирован!')

        return cleaned_data

    def save(self, *args, **kwargs):

        user = super().save(commit=False)

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']

        user.username = username
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        return user


class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):

        cleaned_data = self.cleaned_data

        username = cleaned_data['username']
        password = cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким именем не зарегестрирован!')

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user and not user.check_password(password):
            self.add_error('password', 'Неверный пароль!')

        return cleaned_data
