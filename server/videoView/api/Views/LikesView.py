import logging
from django.http import JsonResponse
from django.db import transaction
from rest_framework.decorators import api_view
from api.serializer import VideoSerializer,AllVideoSerializer,UpdateVideoSerializer,GetVideoByIdSerializer,Subscriptions,UserSerializer
from api.models import Users,Videos,Subscriptions,Likes
from api.utility import ValidateUser
from django.contrib.auth import authenticate
from utils.ApiResponseClass import ApiResponse
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import jwt


load_dotenv()

logger = logging.getLogger('api.LikesView')  

#TODO
#create api for like for comment
#create api for like for tweet





@api_view(['GET'])
@ValidateUser
def like_video_by_user(request,video_id):
    try:

        user_id=request.user_id

        # using atomic here for only save when everything
        with transaction.atomic():
            current_user=Users.objects.get(id=user_id)
            video_instance=Videos.objects.get(id=video_id)
            
            #check for instance
            if not current_user or not video_instance:
                return Response(ApiResponse.error(401,"error while finding user or video",{}).__dict__,status=400)
            # check for instance of certain likes exists already
            likes_instance_exists=Likes.objects.filter(video=video_instance,likedBy=current_user).exists()

            if likes_instance_exists:
                likes_instance=Likes.objects.get(video=video_instance,likedBy=current_user)
                likes_instance.delete()
                return Response(ApiResponse.success(200,"video like removed successfully",{}).__dict__,status=400)
            else:
                likes=Likes.objects.create(video=video_instance,likedBy=current_user)
                return Response(ApiResponse.success(200,"video liked successfully",likes.id).__dict__,status=200)
            
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"likes failed",[]).__dict__,status=500)
