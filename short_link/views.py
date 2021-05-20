from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from .services import shorting_url


class IndexView(TemplateView):
    """Главная страница"""
    template_name = 'short_link/index.html'


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


class CreateShortUrl(LoginRequiredMixin, CreateView):
    """Сокращение ссылки"""
    model = Link
    template_name = 'short_link/url_shorting.html'
    success_message = 'Ссылка создана!'
    form_class = LinkCreateForm
    success_url = reverse_lazy('short_link:index')

    def get_form_kwargs(self):
        kwargs = super(CreateShortUrl, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['short_url'] = shorting_url(self.request.POST.get('url'))
        return kwargs

