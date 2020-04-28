from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login 
from . import forms

 
def main(request) :
    return render(request, 'messenger/main.html')


class UserLoginView(LoginView):
    template_name = 'messenger/login.html'
    form_class = forms.AuthUserForm
    success_url = '/messages'
    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'messenger/register_page.html'
    form_class = forms.RegisterUserForm
    success_url = '/messages'
    success_msg = 'User has been created'
    def form_valid(self, form) :
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        auth_user = authenticate(username = username, password = password)
        login(self.request, auth_user)
        return form_valid

class UserLogOutView(LogoutView):
    next_page = '/'