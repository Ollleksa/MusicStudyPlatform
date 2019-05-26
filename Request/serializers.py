from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Request


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', )


class RequestSerializer(serializers.ModelSerializer):
    requester = AuthorSerializer(many=False, required=False)
    agent = AuthorSerializer(many=False, required=False)

    class Meta:
        model = Request
        fields = ('id', 'requester', 'agent', 'title', 'content', 'timestamp')
        read_only_fields = ('id', 'timestamp')

    def create(self, validated_data):
        agent = get_user_model().objects.get(username=self.context['agent'])
        req = Request(**validated_data)
        req.requester = self.context['request'].user
        req.agent = agent
        req.save()
        return req

