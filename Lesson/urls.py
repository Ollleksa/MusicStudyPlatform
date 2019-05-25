from django.urls import path

from .views import HomePage, LessonPage, CreateLessonPage, LessonCatalog, JsLessonPage, JsLessonCatalogPage, \
    JsImageLoadLessonPage, JsHomePage
from .api_views import LessonViewSet, LikeViewSet, FileUploadView, AllLessonsView

urlpatterns = [
    path('', HomePage.as_view()),
    path('lesson/<int:lesson_id>', LessonPage.as_view()),
    path('lesson/create', CreateLessonPage.as_view(), name='create_lesson'),
    path('lesson', LessonCatalog.as_view(), name='lessons_all'),

    path('js', JsHomePage.as_view(), name='index'),
    path('js_lesson/<int:lesson_id>', JsLessonPage.as_view()),
    path('js_lessons', JsLessonCatalogPage.as_view()),
    path('js_load', JsImageLoadLessonPage.as_view()),

]

api_patterns = [
    path('all', AllLessonsView.as_view(), name='api_lessons'),
    path('user/<int:user_id>', LessonViewSet.as_view({'get': 'list_by_user'})),
    path('<int:lesson_id>', LessonViewSet.as_view({'get': 'get', 'delete': 'delete'})),
    path('create', LessonViewSet.as_view({'post': 'create'}), name='lesson'),
    path('<int:lesson_id>/put_photo', FileUploadView.as_view(), name='load_image_lesson'),

    path('<int:lesson_id>/likes', LikeViewSet.as_view({'get': 'list', 'post': 'like', 'delete': 'unlike'})),
]