from django.urls import path

from .views import HomePage, LessonPage, CreateLessonPage, LessonCatalog

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('lesson/<int:lesson_id>', LessonPage.as_view(), name='lesson'),
    path('lesson/create', CreateLessonPage.as_view(), name='create_lesson'),
    path('lesson', LessonCatalog.as_view(), name='lessons_all')
]