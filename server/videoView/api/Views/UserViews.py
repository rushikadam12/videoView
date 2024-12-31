import logging
from django.http import JsonResponse
from functools import wraps
from rest_framework.decorators import api_view
from api.serializer import UsersRegistrationSerializer
from api.models import Users
from api.utility import generated_refreshToken,check_pass
from django.contrib.auth import authenticate
from utils.ApiResponseClass import ApiResponse
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

logger = logging.getLogger('api.UserViews')  


def ValidateUser(func):
    
    @wraps(func)
    def wraps_func(request,*args,**kwargs):
        try:
            
            access_token=request.COOKIES.get('access_token')
            
            if not access_token:
                return Response(ApiResponse.error(401,error="Unauthorized user",message="").__dict__,status=401) 

            decode_data=jwt.decode(access_token,os.getenv('SECURE_KEY'),algorithms=['HS256'])
            user_id=decode_data.get('id')
            if not user_id:
                return Response(ApiResponse.error(403,error="Invalid token",message="").__dict__,status=403)
            request.user_id=user_id
        except Exception as e:
            logger.debug(f'{e}')
            return Response(ApiResponse.error(403,error=f"token not found",message="").__dict__,status=403)

        return func(request,*args,**kwargs)

    return wraps_func

@api_view(['GET'])
def health_check(request):
    logger.debug("Health check endpoint accessed")
    return JsonResponse({"status":"ok"},status=200)


@api_view(['POST'])
def signup(request):
    
    
    serializer=UsersRegistrationSerializer(data=request.data)
    

    if serializer.is_valid():
        
        user,token=serializer.save()
        
        user_data={
            "fullName":user.fullName,
            "email":user.email
        }

        
        response=Response(ApiResponse.success(201,"user created successfully",{"user":user_data,"token":token}).__dict__,status=201)
        response.set_cookie(key="access_token",value=token['access_token'],max_age=int(os.getenv('ACCESS_TOKEN_EXP')))
        response.set_cookie(key="refresh_token",value=token['refresh_token'],max_age=int(os.getenv('REFRESH_TOKEN_EXP')))
        return response
    return Response(ApiResponse.error(401,"error while creating user",serializer.errors).__dict__,status=401)

@api_view(['POST'])
def login(request):
    try:
            email=request.data.get('email')
            password=request.data.get('password')

            if not email or not password:
                return JsonResponse({'message':"invalid data"}) 

            user=Users.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"message":"email not exits"})

            result=check_pass(current_password=password,user_password=user.password)
            
            if not result:
                return JsonResponse({'message':'wrong password'},status=401)

            token=generated_refreshToken(user)
            user.refreshToken=token['refresh_token']
            user.save()

            
            
            response=JsonResponse({"message":"login successfully","token":token})

            response.set_cookie('access_token',token['access_token'],httponly=True,secure=False,max_age=3600)
            response.set_cookie('refresh_token',token['refresh_token'],httponly=True,secure=False,max_age=36400)

            return response
        
    except Exception as e:
        logger.fatal(str(e))
    

@api_view(['GET'])
@ValidateUser
def get_user(request):
    user=Users.objects.filter(pk=request.user_id).first()
    if user:
        user_obj={
            "id":user.id,
            "email":user.email,
            "fullName":user.fullName,
            "avatar":user.avatar,
            "coverImage":user.coverImage,
            "created_at":user.created_at,
            "updated_at":user.updated_at

            }
    else:
        user_obj={"message":"user not found"}
    return Response(ApiResponse.success(200,message="user retrieved successfully",response=user_obj).__dict__,status=200)

@api_view(['GET'])
@ValidateUser
def logout_user(request):
    try:
        response={"message":"logout successfully"}
        response=Response(ApiResponse.success(200,"logout successfully",response).__dict__,status=200)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

    except Exception as e:
        logger.debug(f"{e}")
        return Response(ApiResponse.error(500,"something went wrong",error=f"{e}").__dict__,status=500)