import logging
from django.http import JsonResponse
from functools import wraps
from rest_framework.decorators import api_view
from api.serializer import UsersRegistrationSerializer,UserUpdateImageSerializer
from api.models import Users
from api.utility import generated_refreshToken,check_pass,validate_token
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
            refresh_token=request.COOKIES.get('refresh_token')
            
            if not access_token and not refresh_token:
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

@api_view(['PATCH'])
@ValidateUser
def update_user(request):
    try:
        
        user=request.user_id
        serializer=UserUpdateImageSerializer(instance=user,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(ApiResponse.success(201,"update user cover",[]).__dict__,status=201)
        
        return Response(ApiResponse.error(400,"Failed to update",error=serializer.errors).__dict__,status=400)
    except Exception as e:
        logger.debug(f"Error :{e}")
        return Response(ApiResponse.error(500,"something went wrong",{"message":f"{e}"}).__dict__,status=500)

@api_view(['GET'])
@ValidateUser
def request_access_token(request):
    try:
        #find user
        user=Users.objects.filter(pk=request.user_id).first()

        token={
            "access_token":request.COOKIES.get('access_token'),
            "refresh_token":request.COOKIES.get('refresh_token')
        }

        # check refresh token and generate new token
        new_token=validate_token(user=user,token=token)
        logger.debug(new_token)
        # set token
        user.refreshToken=new_token.get('refresh_token')
        user.save()

        response=Response(ApiResponse.success(201,"new token generate",response=[]).__dict__,status=201)

        # set-cookie
        response.set_cookie('access_token',new_token['access_token'],httponly=True,secure=False,max_age=3600)
        response.set_cookie('refresh_token',new_token['refresh_token'],httponly=True,secure=False,max_age=36400)

        return response

    except Exception as e:

        logger.debug(f"{e}")
        return Response(ApiResponse.error(500,"something went wrong",{"message":f"{e}"}).__dict__,status=500)
    
@api_view(['POST'])
def reset_password(request):
    try:
        email=request.data.get("email")
    
        user=Users.objects.filter(email=email).first()
        if not user:
            return Response(ApiResponse.error(401,message="",error="user not found").__dict__,status=401)

        subject = 'Welcome to Our Website!'
        message = 'Thank you for signing up with our website. We are excited to have you!'
        from_email = settings.DEFAULT_FROM_EMAIL  # You can use DEFAULT_FROM_EMAIL from settings
        recipient_list = [user_email] 

    except Exception as e:
        logger.debug("Error : {e}")
    


    

