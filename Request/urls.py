from django.urls import path
from django.views.generic import RedirectView

from .views import RequestPage, CreateRequest, RequestCatalog

urlpatterns = [
    path('<int:request_id>', RequestPage.as_view(), name='request'),
    path('create', CreateRequest.as_view(), name='create_request'),
    path('all', RequestCatalog.as_view(), name='request_all'),
    path('', RedirectView.as_view(pattern_name='request_all', permanent=False))
]