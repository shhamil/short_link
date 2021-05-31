# Generated by Django 3.1.11 on 2021-05-31 06:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Описание')),
                ('short_url', models.TextField(verbose_name='Короткая ссылка')),
                ('url_for_shorting', models.TextField(verbose_name='Ссылка')),
                ('slug', models.SlugField(unique=True)),
                ('date_create', models.DateTimeField(default=datetime.datetime(2021, 5, 31, 6, 11, 48, 176785, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
