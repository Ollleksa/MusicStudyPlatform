from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from celery import shared_task

from .models import Request
from .serializers import RequestSerializer


@shared_task
def email_send(user_id):
    user = get_user_model().objects.get(id=user_id)
    mail_subject = 'New request'
    context = {
        'user': user.username,
    }
    message = render_to_string('auth/activation_email.html', context)

    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class AllRequestView(generics.ListAPIView):
    queryset = Request.objects.all().order_by('-timestamp')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    serializer_class = RequestSerializer


class RequestViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        queryset = Request.objects.all()
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, request_id=None):
        queryset = Request.objects.all()
        req = get_object_or_404(queryset, id=request_id)
        serializer = RequestSerializer(req)
        return Response(serializer.data)

    def create(self, request):
        ser = RequestSerializer(data=self.request.data, context={'request': request, 'agent': self.request.data['agent']})
        ser.is_valid(raise_exception=True)
        ser.save()
        user = get_user_model().objects.get(username=ser.data['agent']['username'])

        email_send.delay(user.id)

        return Response(ser.data)

    def delete(self, request, request_id=None):
        queryset = Request.objects.all()
        req = get_object_or_404(queryset, id=request_id)
        if req.requester != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        req.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, request_id=None):
        queryset = Request.objects.all()
        req = get_object_or_404(queryset, id=request_id)
        if req.requester != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        ser = RequestSerializer(req, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)