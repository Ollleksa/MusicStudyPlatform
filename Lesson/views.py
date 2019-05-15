from django.shortcuts import render
from django.views import View

from .models import Lesson


class HomePage(View):
    template = 'home.html'

    def get(self, request):
        current_user = request.user
        lesson_list = Lesson.objects.all()

        context = {
            'lesson_list': lesson_list,
            'user': current_user,
        }

        return render(request, self.template, context)