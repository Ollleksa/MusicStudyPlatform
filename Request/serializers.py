from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    requester = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), default=CurrentUserDefault())

    class Meta:
        model = Request
        fields = ('id', 'requester', 'agent', 'title', 'content', 'timestamp')
        read_only_fields = ('id', 'timestamp')

