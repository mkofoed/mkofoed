from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from accounts.forms import UserForm, RegisterForm
from .models import User


class AccountLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    success_url = reverse_lazy('blog:list')


class AccountView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('accounts:account')

    def get_object(self, queryset=None):
        return self.request.user


class AccountCreateView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:account')

    def form_valid(self, form):
        valid = super(AccountCreateView, self).form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid
