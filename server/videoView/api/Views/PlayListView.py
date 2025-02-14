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

@api_view(["GET"])
@ValidateUser
def create_playlist():
    return ""