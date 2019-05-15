from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout

from .forms import PlatformUserCreationForm, PlatformAuthForm


class SignUpPage(View):
    form_cls = PlatformUserCreationForm
    template = 'auth/signup.html'

    def get(self, request):
        form = self.form_cls()
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = self.form_cls(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

        context = {
            'form': form,
        }
        return render(request, self.template, context)


class LoginPage(View):
    form_cls = PlatformAuthForm
    template = 'auth/login.html'

    def get(self, request):
        form = self.form_cls()
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = self.form_cls(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

        context = {
            'form': form,
        }
        return render(request, self.template, context)


class LogoutPage(View):
    template = 'auth/logout.html'

    def get(self, request):
        context = {}
        logout(request)
        return render(request, self.template, context)