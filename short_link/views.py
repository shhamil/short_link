from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from .services import shorting_url


class IndexView(ListView):
    """Главная страница"""
    model = Link
    template_name = 'short_link/index.html'
    context_object_name = 'links'

    def get_queryset(self):
        queryset = Link.objects.filter(user=self.request.user.pk)
        return queryset


class UserLoginView(LoginView):
    """Страница входа"""
    template_name = 'short_link/login.html'


class RegisterView(SuccessMessageMixin, CreateView):
    """Регистрация"""
    model = User
    template_name = 'short_link/register.html'
    success_message = 'Вы зарегистрированы!'
    form_class = RegistrationForm
    success_url = reverse_lazy('short_link:index')


class CreateShortLink(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Сокращение ссылки"""
    model = Link
    template_name = 'short_link/link_create.html'
    success_message = 'Ссылка создана!'
    form_class = LinkCreateForm
    success_url = reverse_lazy('short_link:index')

    def get_form_kwargs(self):
        kwargs = super(CreateShortLink, self).get_form_kwargs()
        kwargs['pk'] = self.request.user.pk

        return kwargs


class DeleteLink(LoginRequiredMixin, DeleteView):
    model = Link
    template_name = 'short_link/link_delete.html'
    success_url = reverse_lazy('short_link:index')


class TokenView(ListView):
    """Главная страница"""
    model = Token
    template_name = 'short_link/token.html'
    context_object_name = 'token'

    def get_queryset(self):
        queryset = Token.objects.filter(user=self.request.user.pk)
        return queryset


class UpdateLink(LoginRequiredMixin, UpdateView):
    model = Link
    template_name = 'short_link/link_update.html'
    form_class = LinkUpdateForm
    success_url = reverse_lazy('short_link:index')

    def get_form_kwargs(self):
        kwargs = super(UpdateLink, self).get_form_kwargs()
        kwargs['pk'] = self.request.user.pk
        return kwargs
