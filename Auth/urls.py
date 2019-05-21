from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import SignUpPage, LoginPage, LogoutPage
from .api_views import UserViewSet, SignUpViewSet, FileUploadView

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('signup/', SignUpPage.as_view(), name='signup'),
    path('logout/', LogoutPage.as_view(), name='logout'),
]

api_patterns = [
    path('api/signup', SignUpViewSet.as_view({'post': 'create'}), name='sign_up'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='all_users'),
    path('api/user', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'}), name='user'),
    path('api/put_file', FileUploadView.as_view(), name='file_upload'),
    path('api/user/<int:id>', UserViewSet.as_view({'get': 'retrieve'}))
]

urlpatterns += api_patterns