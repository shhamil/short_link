from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import *
from .services import shorting_url


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Aдpec Электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']

        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class LinkUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('pk', None)
        super(LinkUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        user = User.objects.get(pk=self.user_pk)
        if Link.objects.filter(user=user, url_for_shorting=self.cleaned_data['url_for_shorting']).exists():
            raise ValidationError('Такая ссылка уже существует!')

    def save(self, *args, **kwargs):
        user = User.objects.get(pk=self.user_pk)
        link = super().save(commit=False)
        link.short_url = shorting_url(link.url_for_shorting)
        link.slug = user.username + link.short_url.replace('https://tinyurl.com/', '')
        link.save()
        return link

    class Meta:
        model = Link
        fields = ('title', 'url_for_shorting')


class LinkCreateForm(forms.ModelForm):
    url_for_shorting = forms.CharField(label="Ссылка для сокращения")

    def __init__(self, *args, **kwargs):
        self.user_pk = kwargs.pop('pk', None)
        super(LinkCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        user = User.objects.get(pk=self.user_pk)
        if Link.objects.filter(user=user, url_for_shorting=self.cleaned_data['url_for_shorting']).exists():
            raise ValidationError('Такая ссылка уже существует!')

    def save(self, *args, **kwargs):
        user = User.objects.get(pk=self.user_pk)
        link = super().save(commit=False)
        link.user = user
        link.short_url = shorting_url(link.url_for_shorting)
        link.slug = user.username + link.short_url.replace('https://tinyurl.com/', '')
        link.save()
        return link

    class Meta:
        model = Link
        fields = ('title', 'url_for_shorting')
