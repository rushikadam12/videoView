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
def add_comment_to_video(request,video_id):
    try:

        user_id=request.userId
        return Response(ApiResponse.success(500,"comment added successfully",[]).__dict__,status=500)        
        
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"failed to add comment",[]).__dict__,status=500)
