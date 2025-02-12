from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import *
from api.utility import generated_refreshToken

import cloudinary
import cloudinary.uploader
import logging
# from utils.tusServer import tus_upload_server

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
        if image2:
            coverImage_img=cloudinary.uploader.upload(image2)
        
        
        # create user and generate token
        user=Users.objects.create(**validate_data)
        token=generated_refreshToken(user)

        # image
        if image1:
            user.avatar=avatar_img.get('secure_url')
        if image2:
            user.coverImage=coverImage_img.get('secure_url')

        # token
        user.refreshToken=token.get('refresh_token')
        

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


# created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     videoFile=models.URLField(max_length=200)
#     thumbnail=models.URLField()
#     owner=models.ForeignKey(
#         "Users",
#         related_name="video_owner",
#         on_delete=models.CASCADE
#     )
    
#     title=models.CharField(max_length=255)
#     description=models.TextField()
#     duration=models.IntegerField()
#     views=models.IntegerField()
#     isPublished=models.BooleanField()

class VideoSerializer(serializers.ModelSerializer):
    videoFile = serializers.FileField(required=False, allow_null=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    # owner=serializers.PrimaryKeyRelatedField(query=Users.objects.all(),required=False,read_only=True)

    class Meta:
        model=Videos
        fields=['videoFile','thumbnail','title','description','duration','isPublished']


    def create(self,validate_data):
        user=self.context.get('userId')

        videoFile=validate_data.get("videoFile")
        thumbnail=validate_data.get("thumbnail")
        
        user=Users.objects.filter(pk=user).first()
        video_instance=Videos()

        if thumbnail:
            thumbnail_img=cloudinary.uploader.upload(thumbnail,asset_folder="thumbnail",resource_type="image")
            video_instance.thumbnail=thumbnail_img.get("secure_url")
        
        if videoFile:
        #    resp=tus_upload_server(videoFile)
        #    logger.debug(resp)

           videoFile=cloudinary.uploader.upload(videoFile,asset_folder="video",resource_type="video")
           video_instance.videoFile=videoFile.get("secure_url")
           
        
        
        
        video_instance.title=validate_data.get('title')
        video_instance.description=validate_data.get('description')
        video_instance.owner=user
        video_instance.views=0
        video_instance.isPublished=validate_data.get('isPublished')
        video_instance.duration=validate_data['duration']

        video_instance.save()


        return video_instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'fullName', 'email','avatar','coverImage']

class AllVideoSerializer(serializers.ModelSerializer):
    owner=UserSerializer(read_only=True)
    class Meta:
        model=Videos
        fields=['id','videoFile','thumbnail','owner','title','description','duration','views','isPublished','created_at','updated_at']
class GetVideoByIdSerializer(serializers.ModelSerializer):
    owner=UserSerializer(read_only=True)
    class Meta:
        model=Videos
        fields=['id','videoFile','thumbnail','owner','title','description','duration','views','isPublished','created_at','updated_at']

    def to_representation(self,instance):
        
        # logger.debug(f"checking........{instance.video_viewed_by}")
        # user_exits=self.context.get('user_id').id
        
        # if instance.id not in user_exits.watchHistory:
        # TODO:Check for model to update views only one per user
        
        instance.views+=1
        instance.save()
        
        return super(GetVideoByIdSerializer, self).to_representation(instance)

class UpdateVideoSerializer(serializers.ModelSerializer):

    thumbnail= serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model=Videos
        fields=['thumbnail','title','description']
        extra_kwargs = {
            'thumbnail': {'required': False, 'allow_null': True},
            'title': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_null': True}
        }

        def update(self,instance,validate_data):

            if 'thumbnail' in validate_data:
                image=validate_data.get('thumbnail')
                if image:
                    updated_img=cloudinary.uploader.upload(image,asset_folder="thumbnail",resource_type="image")
                    instance.thumbnail=updated_img.get("secure_url")
            
            if 'title' in validate_data:
                new_title=validate_data.get('title')
                instance.title=new_title
            
            if 'description' in validate_data:
                new_description=validate_data.get('title')
                instance.description=new_description
            
            instance.save()
            
            return instance

# class CreateLikesModelInstance(models.Model):
#     class Meta:
#         model=Likes
#         fields=['comment']

class GetVideoComments(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=['id','content','owner','video']