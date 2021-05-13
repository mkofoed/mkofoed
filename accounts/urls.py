from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import AccountCreateView, AccountLoginView, AccountView

app_name = 'accounts'
urlpatterns = [
    path('update/', AccountView.as_view(), name='account'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('signup/', AccountCreateView.as_view(), name='signup'),
]
