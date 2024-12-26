from django.db import models
import uuid

class Videos(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    videoFile=models.URLField(max_length=200)
    thumbnail=models.URLField()
    owner=models.ManyToManyField(
        "Users",
        related_name="video_owner",
        blank=False,
        null=False
    )
    
    title=models.CharField(255)
    description=models.TextField()
    duration=models.IntegerField()
    views=models.IntegerField()
    isPublished=models.BooleanField()
    
    
    

class Users(models.Model):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    watchHistory=models.ManyToManyField(
        "Videos",
        related_name='watchedVideo',
        blank=True
    )
    username=models.CharField(max_length=255)
    email=models.EmailField(max_length=254)
    fullName=models.CharField(max_length=255)
    avatar=models.URLField(max_length=200)
    coverImage=models.URLField(max_length=200)
    password=models.TextField()
    refreshToken=models.TextField()