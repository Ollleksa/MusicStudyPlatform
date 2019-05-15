from django.urls import path

from .views import SignUpPage, LoginPage, LogoutPage

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('signup/', SignUpPage.as_view(), name='signup'),
    path('logout/', LogoutPage.as_view(), name='logout'),
]