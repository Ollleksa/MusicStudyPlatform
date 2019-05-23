from django.urls import path
from django.views.generic import RedirectView

from .views import RequestPage, CreateRequest, RequestCatalog

from .api_views import RequestViewSet

urlpatterns = [
    path('<int:request_id>', RequestPage.as_view(), name='request'),
    path('create', CreateRequest.as_view(), name='create_request'),
    path('all', RequestCatalog.as_view(), name='request_all'),

    path('', RedirectView.as_view(pattern_name='request_all', permanent=False))
]

api_patterns = [
    path('all', RequestViewSet.as_view({'get': 'list'}), name='api_requests'),
    path('<int:request_id>', RequestViewSet.as_view({'get': 'get', 'delete': 'delete'}), name='one_request'),
    path('create', RequestViewSet.as_view({'post': 'create'}), name='request'),
]