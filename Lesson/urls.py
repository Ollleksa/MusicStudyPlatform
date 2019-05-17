from django.urls import path

from .views import HomePage, LessonPage, CreateLessonPage, LessonCatalog
from .api_views import LessonsAPIView, OneLessonAPIView

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('lesson/<int:lesson_id>', LessonPage.as_view(), name='lesson'),
    path('lesson/create', CreateLessonPage.as_view(), name='create_lesson'),
    path('lesson', LessonCatalog.as_view(), name='lessons_all'),
    path('api/all_lessons', LessonsAPIView.as_view(), name='api_all_lessons'),
    path('api/lesson/<int:lesson_id>', OneLessonAPIView.as_view(), name='api_lesson'),
]
