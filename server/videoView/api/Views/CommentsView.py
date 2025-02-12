import logging
from django.http import JsonResponse
from django.db import transaction
from rest_framework.decorators import api_view
from api.serializer import VideoSerializer,AllVideoSerializer,UpdateVideoSerializer,GetVideoByIdSerializer,Subscriptions,UserSerializer,GetVideoComments
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

@api_view(['DELETE'])
@ValidateUser
# TODO:Test after creating the API for get_all_comments
def delete_video_comment(request,comment_id):
    try:
        comment_instance=Comments.objects.get(id=comment_id)        
        comment_instance.delete()

        return Response(ApiResponse.success(200,"comment deleted successfully",[]).__dict__,status=200)
    except Comments.DoesNotExist as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(400,"comment not found",[]).__dict__,status=400)
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"failed to add comment",[]).__dict__,status=500)


@api_view(['GET'])
@ValidateUser
def get_all_comments(request,video_id):
    try:
        comments_instance=Comments.objects.filter(video_id=video_id)
        
        # final result
        result=[]

        for comment in comments_instance:
            serializers=GetVideoComments(comment)
            result.append(serializers.data)

        return Response(ApiResponse.success(200,"get comments successfully",result).__dict__,status=200)
    except Comments.DoesNotExist as e:
        logger.debug(f"Error found : comment not found") 
        return Response(ApiResponse.error(400,"Invalid video Id",[]).__dict__,status=400)
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"failed to get comment",[]).__dict__,status=500)