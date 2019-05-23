from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import SignUpPage, LoginPage, LogoutPage, JSLoginPage, JSSignUpPage
from .api_views import UserViewSet, SignUpViewSet, FileUploadView

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('js_login', JSLoginPage.as_view()),
    path('js_sign_up', JSSignUpPage.as_view()),
    path('signup/', SignUpPage.as_view(), name='signup'),
    path('logout/', LogoutPage.as_view(), name='logout'),
]

api_patterns = [
    path('signup/', SignUpViewSet.as_view({'post': 'create'}), name='sign_up'),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('users', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='all_users'),
    path('user', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'}), name='user'),
    path('put_file', FileUploadView.as_view(), name='file_upload'),
    path('user/<int:id>', UserViewSet.as_view({'get': 'retrieve'}), name = 'one_user')
]
