from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    short_url = models.TextField(verbose_name='Короткая ссылка')
    url = models.TextField(verbose_name='Ссылка')
    date_create = models.DateTimeField(default=timezone.now())
