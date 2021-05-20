from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'short_link'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/logout/', LogoutView.as_view(next_page="/accounts/login/"), name='logout'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/', IndexView.as_view(), name='profile'),
    path('accounts/url_generator', CreateShortUrl.as_view(), name='short_url'),
]
