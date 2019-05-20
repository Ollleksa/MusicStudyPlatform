from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Request
from .serializers import RequestSerializer


class RequestViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

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
        ser = RequestSerializer(data=self.request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
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