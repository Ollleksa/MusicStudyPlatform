from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

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
            user = form.save()

            mail_subject = 'Welcome!'
            context = {
                'user':user.username,
            }
            message = render_to_string('auth/activation_email.html', context)

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

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


class JSLoginPage(View):
    template = 'auth/js_signin.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)


class JSSignUpPage(View):
    template = 'auth/js_signup.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)


class JSLoadPage(View):
    template = 'auth/load_avatar.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)