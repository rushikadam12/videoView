from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *




class UsersRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=['fullName','email','password']
        optional_felids=['avatar','coverImage']
    
    def validate_email(self,value):
            if Users.objects.filter(email=value).exists():
                raise ValidationError("email already exists")
            return value
    def create(self,validate_data):
        password=validate_data['password']
        validate_data['password']=make_password(password)
        user=Users.objects.create(**validate_data)
        return user