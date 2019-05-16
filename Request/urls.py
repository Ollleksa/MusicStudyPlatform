from django.urls import path

from .views import RequestPage, CreateRequest, RequestCatalog

urlpatterns = [
    path('<int:request_id>', RequestPage.as_view(), name='request'),
    path('create', CreateRequest.as_view(), name='create_request'),
    path('', RequestCatalog.as_view(), name='request_all'),
]