from django.urls import path
from django.conf.urls import url

from .views import HomePage

urlpatterns = [
    url('', HomePage.as_view(), name='index'),
]