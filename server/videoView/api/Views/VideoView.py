import logging
from django.http import JsonResponse

from rest_framework.decorators import api_view
from api.serializer import VideoSerializer,AllVideoSerializer,UpdateVideoSerializer,GetVideoByIdSerializer
from api.models import Users,Videos
from api.utility import ValidateUser
from django.contrib.auth import authenticate
from utils.ApiResponseClass import ApiResponse
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

logger = logging.getLogger('api.UserViews')  

@api_view(["POST"])
@ValidateUser
def upload_video(request):

    try:

        user=request.user_id
        serializer=VideoSerializer(data=request.data,context={"userId":user})

        if not serializer.is_valid():
            return Response(ApiResponse.error(401,"invalid data",error=serializer.errors).__dict__,401)
    
        serializer.save()
        return Response(ApiResponse.success(201,"video uploaded successfully",serializer.data).__dict__,status=201)

    except Exception as e:
        logger.debug(f"{e}")
        return Response(ApiResponse.error(500,"something went wrong",error=f"{e}").__dict__,500)
    

@api_view(['GET'])
@ValidateUser
def get_all_videos(request):

    video_list=Videos.objects.all()

    serializer=AllVideoSerializer(video_list,many=True)

    return Response(ApiResponse.success(200,"fetched all videos",response=serializer.data).__dict__,status=200)

@api_view(['GET'])
@ValidateUser
def get_video_by_videoId(request,id):
    try:
        user=request.user_id
        try:
            video_data=Videos.objects.get(id=id)
        except video_data.DoesNotExist:
            return Response(ApiResponse.error(401,"invalid id data not found",[]).__dict__,status=401)
        
        serializer=GetVideoByIdSerializer(instance=video_data,context={"userId":user})
        
        if not video_data:
            return Response(ApiResponse.error(401,"invalid id data not found",[]).__dict__,status=401)
        logger.debug(f"checking..........{serializer.data}")
        return Response(ApiResponse.error(200,"fetch video by id",serializer.data).__dict__,status=200)
    except Exception as e:
        
        logger.debug(f"Error as occurred : {e}")
        return Response(ApiResponse.error(401,"invalid id data not found",{"error":str(e)}).__dict__,status=401)

    
@api_view(['PATCH'])
@ValidateUser
def update_video(request,id):
    try:
        video_instance=Videos.objects.get(id=id)
        
        serializer=UpdateVideoSerializer(data=request.data,instance=video_instance)
        if serializer.is_valid():
            update_video_instance=serializer.save()
            return Response(ApiResponse.success(201,"video update successfully",update_video_instance.title).__dict__,status=200)
            
        return Response(ApiResponse.error(400,"error",serializer.errors).__dict__,status=400)

    except Exception as e:
        logger.debug(f"Error found : {e}")
        return Response(ApiResponse.error(401,"upload failed",{"error":str(e)}).__dict__,status=500)

@api_view(['DELETE'])
@ValidateUser
def delete_video(request,video_id):
    try:
        try:
            current_video=Videos.objects.get(id=video_id)
        except current_video.DoesNotExist:
            return Response(ApiResponse.error(400,"video not found",[]).__dict__,status=400)    
        current_video.delete()
        return Response(ApiResponse.success(200,"video delete successfully",[]).__dict__,status=200)
    except Exception as e:
        return Response(ApiResponse.error(401,"upload failed",{"error":str(e)}).__dict__,status=500)

@api_view(['GET'])
@ValidateUser
def is_published(request,video_id):
    try:

        try:
            current_video=Videos.objects.get(id=video_id)
        except current_video.DoesNotExist:
            return Response(ApiResponse.error(400,"video not found",[]).__dict__,status=400)    

        current_video.isPublished=not current_video.isPublished
        current_video.save()
        return Response(ApiResponse.success(200,"video updated successfully",[]).__dict__,status=200)
    except Exception as e:
        return Response(ApiResponse.error(401,"upload failed",{"error":str(e)}).__dict__,status=500)



