from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from api.utility import generated_refreshToken
import cloudinary
import cloudinary.uploader



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

