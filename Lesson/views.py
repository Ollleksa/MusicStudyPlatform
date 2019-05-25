from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Lesson
from .forms import NewLesson


class HomePage(View):
    template = 'home.html'

    def get(self, request):
        current_user = request.user
        last_lesson_list = Lesson.objects.all().order_by('-timestamp')[:10]

        context = {
            'lesson_list': last_lesson_list,
            'user': current_user,
        }

        return render(request, self.template, context)


class JsTempLessonPage(View):
    template = 'model/js_lesson.html'

    def get(self, request, **kwargs):
        return render(request, self.template)


class LessonPage(View):
    template = 'model/lesson.html'

    def get(self, request, **kwargs):
        lesson = Lesson.objects.get(pk = kwargs['lesson_id'])
        context = {
            'lesson': lesson,
        }
        return render(request, self.template, context)


class JsLessonPage(View):
    template = 'model/js_onelesson.html'

    def get(self, request, **kwargs):
        lesson_id = kwargs['lesson_id']
        context = {
            'lesson_id': lesson_id,
        }
        return render(request, self.template, context)


class JsLessonCatalogPage(View):
    template = 'model/js_all_lessons.html'

    def get(self, request, **kwargs):
        return render(request, self.template)


class JsImageLoadLessonPage(View):
    template = 'model/load_file.html'

    def get(self, request, **kwargs):
        return render(request, self.template)

    def post(self, request, **kwargs):
        return render(request, self.template)


class LessonCatalog(View):
    template = 'model/all_lessons.html'

    def get(self, request):
        all_lessons = Lesson.objects.all().order_by('-timestamp')
        paginator = Paginator(all_lessons, 20)
        page = request.GET.get('page')
        current_page = paginator.get_page(page)

        context = {
            'lessons': current_page,
        }
        return render(request, self.template, context)


class CreateLessonPage(View):
    template = 'model/create_lesson.html'

    def get(self, request):
        form = NewLesson()
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = NewLesson(request.POST)
        if form.is_valid():
            new_lesson = Lesson(author=request.user, title=form.cleaned_data['title'],
                                content=form.cleaned_data['content'])
            new_lesson.save()
            return HttpResponseRedirect('{}'.format(new_lesson.pk))
        else:
            form = NewLesson()

        context = {
            'form': form,
        }
        return render(request, self.template, context)