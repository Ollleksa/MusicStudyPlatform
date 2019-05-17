from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PlatformUser as User
from .serializers import UserSerializer


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        ser = UserSerializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class UserViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_admin:
            return Response(status.HTTP_403_FORBIDDEN)
        ser = UserSerializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def update(self, request, id=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=request.user.id)
        ser = UserSerializer(user, data=self.request.data)
        ser.is_valid(raise_exception=True)

        ser.save()
        return Response(ser.data)

    def delete(self, request, id=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)