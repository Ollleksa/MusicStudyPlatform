from django.views import View
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate


class LogoutPage(View):
    template = 'auth/logout.html'

    def get(self, request):
        context = {}
        logout(request)
        return render(request, self.template, context)


class LoginPage(View):
    template = 'auth/log_in.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)


class SignUpPage(View):
    template = 'auth/sign_up.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)


class LoadPage(View):
    template = 'auth/load_avatar.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return render(request, self.template)