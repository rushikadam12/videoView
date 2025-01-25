from django.db import models
import uuid


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
        related_name='video_viewed_by',
        blank=True
    )
    email=models.EmailField(max_length=254,unique=True)
    fullName=models.CharField(max_length=255)
    avatar=models.URLField(max_length=255,null=True)
    coverImage=models.URLField(max_length=200,null=True)
    password=models.TextField()
    refreshToken=models.TextField()

    def __str__(self):
        return self.fullName
    
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
    owner=models.ForeignKey(
        "Users",
        related_name="video_owner",
        on_delete=models.CASCADE
    )
    
    title=models.CharField(max_length=255)
    description=models.TextField()
    duration=models.IntegerField()
    views=models.IntegerField()
    isPublished=models.BooleanField()
    
    def __str__(self):
        return self.title
    
    
class Subscriptions(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    subscriber=models.ForeignKey('Users',related_name="subscribed_user",on_delete=models.CASCADE,null=True)
    channel=models.ForeignKey('Users',related_name="subscribed_channel",on_delete=models.CASCADE,null=True)

class Likes(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    comment=models.ForeignKey('Comments',null=True,blank=True,on_delete=models.CASCADE)
    tweet=models.ForeignKey('Tweets',null=True,blank=True,on_delete=models.CASCADE)
    video=models.ForeignKey('Videos',null=True,blank=True,on_delete=models.CASCADE)
    likedBy=models.ForeignKey('Users',null=True,blank=True,on_delete=models.CASCADE)

class Comments(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    owner = models.ForeignKey('Users',on_delete=models.CASCADE)
    video = models.ForeignKey('Videos', on_delete=models.CASCADE)
    content=models.TextField()

class PlayList(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name=models.CharField(max_length=250)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    owner=models.ForeignKey('Users',on_delete=models.CASCADE)
    videos=models.ManyToManyField('Videos',related_name="playlist")

class Tweets(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    owner=models.ForeignKey('Users',on_delete=models.CASCADE)
    content=models.CharField(max_length=255,null=False)
