import re
from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Application, Profile, Review


LOGIN_RE = re.compile(r'^[A-Za-z0-9]+$')


class RegistrationForm(forms.Form):
    """Регистрация нового пользователя со всеми обязательными полями."""

    username = forms.CharField(
        label='Логин',
        min_length=6,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Латиница и цифры, минимум 6 символов'}),
        help_text='Логин должен содержать только латинские буквы и цифры, минимум 6 символов.',
    )
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Минимум 8 символов'}),
        help_text='Пароль должен содержать минимум 8 символов.',
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    full_name = forms.CharField(
        label='ФИО',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
    )
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    phone = forms.CharField(
        label='Контактный телефон',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not LOGIN_RE.fullmatch(username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры.')
        if len(username) < 6:
            raise ValidationError('Логин должен содержать минимум 6 символов.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        return password

    def clean_birth_date(self):
        bd = self.cleaned_data['birth_date']
        if bd > date.today():
            raise ValidationError('Дата рождения не может быть в будущем.')
        return bd

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Пароли не совпадают.')
        return cleaned

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        Profile.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            birth_date=self.cleaned_data['birth_date'],
            phone=self.cleaned_data['phone'],
        )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['transport_type', 'start_date', 'payment_method']
        widgets = {
            'transport_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'transport_type': 'Вид транспорта',
            'start_date': 'Дата начала обучения',
            'payment_method': 'Способ оплаты',
        }

    def clean_start_date(self):
        d = self.cleaned_data['start_date']
        if d < date.today():
            raise ValidationError('Дата начала обучения не может быть в прошлом.')
        return d


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Расскажите о впечатлениях…'}),
        }
        labels = {'rating': 'Оценка', 'text': 'Отзыв'}


class StatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {'status': forms.Select(attrs={'class': 'form-select form-select-sm'})}
