from django.urls import path

from .views import HomePage, LessonPage, CreateLessonPage, LessonCatalog
from .api_views import LessonViewSet, LikeViewSet

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('lesson/<int:lesson_id>', LessonPage.as_view()),
    path('lesson/create', CreateLessonPage.as_view(), name='create_lesson'),
    path('lesson', LessonCatalog.as_view(), name='lessons_all'),

    path('api/lessons', LessonViewSet.as_view({'get': 'list'}), name='api_lessons'),
    path('api/lessons/user/<int:user_id>', LessonViewSet.as_view({'get': 'list_by_user'})),
    path('api/lesson/<int:lesson_id>', LessonViewSet.as_view({'get': 'get', 'delete': 'delete'})),
    path('api/lesson', LessonViewSet.as_view({'post': 'create'}), name='lesson'),

    path('api/lesson/<int:lesson_id>/likes', LikeViewSet.as_view({'get': 'list', 'post': 'like', 'delete': 'unlike'})),
]
