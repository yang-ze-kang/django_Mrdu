#!/usr/bin/env python
from django.contrib import auth
from rest_framework import serializers

User = auth.get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email',]
