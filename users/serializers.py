from rest_framework import serializers
from .models import User, Organisation
from django.contrib.auth.hashers import make_password
import random

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','userId', 'firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']
