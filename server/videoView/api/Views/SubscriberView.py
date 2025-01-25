import logging
from django.http import JsonResponse

from rest_framework.decorators import api_view
from api.serializer import VideoSerializer,AllVideoSerializer,UpdateVideoSerializer,GetVideoByIdSerializer,Subscriptions,UserSerializer
from api.models import Users,Videos,Subscriptions
from api.utility import ValidateUser
from django.contrib.auth import authenticate
from utils.ApiResponseClass import ApiResponse
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

logger = logging.getLogger('api.UserViews')  

@api_view(['GET'])
@ValidateUser
def toggle_subscription(request,channel_id):
    try:

        user=request.user_id
        logger.debug(f"logged in user:{Users.objects.get(id=user)}")
        logger.debug(f"channel user:{Users.objects.get(id=channel_id)}")
        current_user=Users.objects.get(id=user)
        channel_users_id=Users.objects.get(id=channel_id)

        # check for subscribed user already exists
        try:
            already_exits=Subscriptions.objects.get(subscriber=current_user.id,channel=channel_id)
            already_exits.delete()
            return Response(ApiResponse.success(200,"channel unsubscribed successfully",[]).__dict__,status=200)

        except Subscriptions.DoesNotExist as e:
            logger.debug(str(e))

            
            # subscribe
            subscription_data={
                'subscriber':current_user,
                'channel':channel_users_id
            }

            new_subscription=Subscriptions.objects.create(**subscription_data)

            return Response(ApiResponse.success(201,"channel subscribed successfully",{}).__dict__,status=201)

    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.success(500,"channel subscription failed",[]).__dict__,status=500)




@api_view(['GET'])
@ValidateUser
def get_videos_by_channel_Id(request,channel_id):
    try:
        channel_obj=Users.objects.get(id=channel_id)
        all_videos=Videos.objects.filter(owner=channel_obj)
        # serializer
        serializer=AllVideoSerializer(all_videos,many=True).data

        return Response(ApiResponse.success(200,"Fetched video successfully",serializer).__dict__,status=200)        
    except Exception as e:
        logger.debug(f"Error found :{e}")
        return Response(ApiResponse.success(401,f"{e}",{}).__dict__,status=500)        

@api_view(['GET'])
@ValidateUser
def get_subscriber_count(request,channel_id):
    try:
         subscriber_count=Subscriptions.objects.filter(channel=channel_id).count()
         return Response(ApiResponse.success(200,"Fetched video successfully",{"subscriber_count":subscriber_count}).__dict__,status=200)        
    except Exception as e:
        logger.debug(f"Error found :{e}")
        return Response(ApiResponse.success(401,f"{e}",{}).__dict__,status=500)

@api_view(['GET'])
@ValidateUser
def get_channel_info(request,channel_id):
    try:
        try:
            current_user=Users.objects.get(id=channel_id)
        except Users.DoesNotExist as e:
            return Response(ApiResponse.error(401,"user not found",{}).__dict__,status=400)     
        
        #get user info 
        serializer_data=UserSerializer(current_user).data
        
        return Response(ApiResponse.success(201,"Fetched video successfully",serializer_data).__dict__,status=200) 


    except Exception as e:
        logger.debug(f"Error found:{e}")
        return Response(ApiResponse.error(401,f"{e}",{}).__dict__,status=500)
