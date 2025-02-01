import logging
from django.http import JsonResponse
from django.db import transaction
from rest_framework.decorators import api_view
from api.serializer import VideoSerializer,AllVideoSerializer,UpdateVideoSerializer,GetVideoByIdSerializer,Subscriptions,UserSerializer
from api.models import Users,Videos,Subscriptions,Likes,Comments
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
        content=request.data.get("content")

        user_id=request.user_id
        current_user_instance=Users.objects.get(id=user_id)
        video_instance=Videos.objects.get(id=video_id)

        add_comment=Comments.objects.create(owner=current_user_instance,video=video_instance,content=content)

        if add_comment is None:
            return Response(ApiResponse.error(400,"failed to add comment",[]).__dict__,status=400) 
        
        return Response(ApiResponse.success(200,"comment added successfully",[]).__dict__,status=200) 
     
    except Users.DoesNotExist as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"user not found",[]).__dict__,status=500)
    except Videos.DoesNotExist as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"video not found",[]).__dict__,status=500)
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"failed to add comment",[]).__dict__,status=500)
