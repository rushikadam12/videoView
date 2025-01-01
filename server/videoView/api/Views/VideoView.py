import logging
from django.http import JsonResponse

from rest_framework.decorators import api_view
from api.serializer import VideoSerializer,AllVideoSerializer
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
def get_all_videos(request):
    video_list=Videos.objects.all()

    serializer=AllVideoSerializer(video_list,many=True)

    return Response(ApiResponse.success(200,"fetched all videos",response=serializer.data).__dict__,status=200)

# get_all_video/:id
#