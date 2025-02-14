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
            
            # check for instance of certain likes exists already
            likes_instance_exists=Likes.objects.filter(video=video_instance,likedBy=current_user).exists()

            if likes_instance_exists:
                likes_instance=Likes.objects.get(video=video_instance,likedBy=current_user)
                likes_instance.delete()
                return Response(ApiResponse.success(200,"video like removed successfully",{}).__dict__,status=200)
            else:
                likes=Likes.objects.create(video=video_instance,likedBy=current_user)
                return Response(ApiResponse.success(200,"video liked successfully",likes.id).__dict__,status=200)
    except Users.DoesNotExist as e:
        return Response(ApiResponse.error(401,"error while finding user or video",{}).__dict__,status=400)
    except Videos.DoesNotExist as e:
        return Response(ApiResponse.error(401,"error while finding user or video",{}).__dict__,status=400)
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"likes failed",[]).__dict__,status=500)

@api_view(['GET'])
def like_comment_by_user(request,comment_id):
    try:
        user_id=request.user_id
        
        with transaction.atomic():
            current_user=Users.objects.get(id=user_id)
            like_instance_exists=Likes.objects.filter(comment=comment_id,liked_by=current_user).exists()

            if like_instance_exists:
                like_instance=Likes.objects.get(comment=comment_id,likeBy=current_user)
                like_instance.delete()
                return Response(ApiResponse.success(200,"comment like removed successfully",{}).__dict__,status=200)
            
            likes=Likes.objects.create(comment=comment_id,likedBy=current_user)
            return Response(ApiResponse.success(200,"comment liked successfully",likes.id).__dict__,status=200)

    except Users.DoesNotExist as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(400,"user not found",[]).__dict__,status=400)
    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(500,"failed to add likes to comment ",[]).__dict__,status=500)