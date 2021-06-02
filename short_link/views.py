from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .forms import *
from .models import *
from .services import *


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def link_api(request):
    url_for_shorting = request.POST.get("url_for_shorting")
    short_url = shorting_url(url_for_shorting)
    data = {'short_link': short_url}
    return Response(data, status=HTTP_200_OK)


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
        queryset = Token.objects.filter(user=self.request.user)
        return queryset


def create_token(request):
    token = Token()
    token.key = default_token_generator.make_token(request.user)
    token.user = request.user
    token.save()
    return HttpResponseRedirect(reverse('short_link:token'))


class UpdateLink(LoginRequiredMixin, UpdateView):
    model = Link
    template_name = 'short_link/link_update.html'
    form_class = LinkUpdateForm
    success_url = reverse_lazy('short_link:index')

    def get_form_kwargs(self):
        kwargs = super(UpdateLink, self).get_form_kwargs()
        kwargs['pk'] = self.request.user.pk
        return kwargs
