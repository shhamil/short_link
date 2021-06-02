from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *


app_name = 'short_link'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/login', login),
    path('api/sampleapi', link_api),
    path('accounts/logout/', LogoutView.as_view(next_page="/accounts/login/"), name='logout'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/', IndexView.as_view(), name='profile'),
    path('accounts/profile/link_generator', CreateShortLink.as_view(), name='short_link'),
    path('accounts/profile/link_delete/<str:slug>', DeleteLink.as_view(), name='delete_link'),
    path('accounts/profile/link_update/<str:slug>', UpdateLink.as_view(), name='update_link'),
    path('accounts/profile/token/', TokenView.as_view(), name='token'),
    path('accounts/profile/token/create', create_token, name='token_create'),
]
