from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser

from rest_framework_simplejwt.tokens import AccessToken

from PIL import Image
from celery import shared_task

from .models import PlatformUser as User
from .serializers import UserSerializer


@shared_task
def email_send(user_id):
    user = User.objects.get(id=user_id)
    mail_subject = 'Welcome!'
    context = {
        'user': user.username,
    }
    message = render_to_string('auth/activation_email.html', context)

    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        ser = UserSerializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()

        email_send.delay(user.id)
        token = AccessToken.for_user(self.user)

        return Response(ser.data)


class UserViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = User.objects.all()
        if not id:
            id = request.user.id
        user = get_object_or_404(queryset, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_admin:
            return Response(status.HTTP_403_FORBIDDEN)
        ser = UserSerializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def update(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=request.user.id)
        ser = UserSerializer(user, data=self.request.data)
        ser.is_valid(raise_exception=True)

        ser.save()
        return Response(ser.data)

    def delete(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileUploadView(views.APIView):
    #parser_classes = (FileUploadParser,)
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            file = request.data['file']
        except KeyError:
            raise KeyError('Request has no avatar attached')

        user = request.user
        user.avatar.save(file.name, file, save=True)
        image = Image.open(user.avatar)
        image.thumbnail((128,128))
        image.save(settings.MEDIA_ROOT + '/media/' + file.name)
        user.avatar = image

        return Response(status.HTTP_202_ACCEPTED)