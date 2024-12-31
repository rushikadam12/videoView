from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import *
from api.utility import generated_refreshToken
import cloudinary
import cloudinary.uploader
import logging

logger = logging.getLogger('api.serializer')  

class UsersRegistrationSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    coverImage = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model=Users
        fields=['fullName','email','password','avatar','coverImage']
        extra_kwargs = {
            'avatar': {'required': False, 'allow_null': True},
            'coverImage': {'required': False, 'allow_null': True},
        }
    
    def validate_email(self,value):
            if Users.objects.filter(email=value).exists():
                raise ValidationError("email already exists")
            return value

    def create(self,validate_data):

        # password hash
        password=validate_data['password']
        validate_data['password']=make_password(password=password,salt=None, hasher='pbkdf2_sha256')
        
        # image upload to cloudinary
        image1=validate_data.get('avatar')
        image2=validate_data.get('coverImage')

        if image1:
            avatar_img=cloudinary.uploader.upload(image1)
        if image1:
            coverImage_img=cloudinary.uploader.upload(image2)
        
        
        # create user and generate token
        user=Users.objects.create(**validate_data)
        token=generated_refreshToken(user)

        # image
        if image1:
            user.avatar=avatar_img['secure_url']
        if image2:
            user.coverImage=coverImage_img['secure_url']

        # token
        user.refreshToken=token['refresh_token']
        

        user.save()

        return user,token


class UserUpdateImageSerializer(serializers.ModelSerializer):

    email=serializers.EmailField(required=False,allow_null=True)
    fullName=serializers.CharField(required=False,allow_null=True)
    avatar = serializers.ImageField(required=False, allow_null=True)
    coverImage = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model=Users
        fields=['email','fullName','avatar','coverImage']
        extra_kwargs = {
            'email': {'required': False, 'allow_null': True},
            'fullName': {'required': False, 'allow_null': True},
            'avatar': {'required': False, 'allow_null': True},
            'coverImage': {'required': False, 'allow_null': True},
        }
    
    # check for attributes
    def validate(self, attrs):
        if not any([attrs.get('avatar'), attrs.get('coverImage'), attrs.get('fullName'), attrs.get('email')]):
            raise ValidationError("At least one field must be provided: avatar, coverImage, fullName, or email.")
        return attrs

    def validate_email(self,value):
            if not  Users.objects.filter(email=value).exists():
                raise ValidationError("User not found")
            return value

    def update(self,instance,validate_data):
        user=Users.objects.filter(pk=instance).first()
        if 'avatar' in validate_data:
            image=validate_data.get('avatar')
            if image:
                avatar_img=cloudinary.uploader.upload(image)
                user.avatar=avatar_img.get('secure_url')

        if 'coverImage' in validate_data:
            image=validate_data.get('coverImage')
            if image:
                cover_img=cloudinary.uploader.upload(image)
                user.coverImage=cover_img.get('secure_url')

        if 'fullName' in validate_data:
            user.fullName=validate_data.get('fullName')

        if 'email' in validate_data:
            user.email=validate_data.get('email')
        
        user.update_at=datetime.now()

        user.save()

        return user