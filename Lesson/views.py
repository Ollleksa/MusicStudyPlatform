from django.shortcuts import render
from django.views import View


class HomePage(View):
    template = 'home.html'

    def get(self, request, **kwargs):
        return render(request, self.template)


class LessonPage(View):
    template = 'model/lesson.html'

    def get(self, request, **kwargs):
        lesson_id = kwargs['lesson_id']
        context = {
            'lesson_id': lesson_id,
        }
        return render(request, self.template, context)


class LessonCatalogPage(View):
    template = 'model/all_lessons.html'

    def get(self, request, **kwargs):
        page = request.GET.get('page')
        context = {
            'page':page,
        }
        return render(request, self.template, context)


class CreateLessonPage(View):
    template = 'model/create_lesson.html'

    def get(self, request, **kwargs):
        return render(request, self.template)

    def post(self, request, **kwargs):
        return render(request, self.template)


class ImageLoadLessonPage(View):
    template = 'model/load_lesson_header.html'

    def get(self, request, **kwargs):
        lesson_id = kwargs['lesson_id']
        context = {
            'lesson_id': lesson_id,
        }
        return render(request, self.template, context)

    def post(self, request, **kwargs):
        lesson_id = kwargs['lesson_id']
        context = {
            'lesson_id': lesson_id,
        }
        return render(request, self.template, context)
