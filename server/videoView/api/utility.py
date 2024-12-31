import logging
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.response import Response
from utils.ApiResponseClass import ApiResponse
from dotenv import load_dotenv
import os

load_dotenv()

logger=logging.getLogger('api.utility')

def generated_refreshToken(user):
    access_token_expiration=timedelta(days=1)
    refresh_token_expiration=timedelta(days=7)

    access_payload={
    "id":str(user.id),
    "email":user.email,
    "exp":datetime.utcnow()+access_token_expiration
    }

    refreshToken_payload={
        "id":str(user.id),
        "email":user.email,
        "exp":datetime.utcnow()+refresh_token_expiration
    }

    access_token=jwt.encode(access_payload,settings.SECRET_KEY,algorithm="HS256")
    refresh_token=jwt.encode(refreshToken_payload,settings.SECRET_KEY,algorithm="HS256")

    return {
        'access_token':access_token,
        'refresh_token':refresh_token
    }

def check_pass(current_password,user_password):
    val=check_password(current_password,user_password)
    return val

def validate_token(token,user):
    try:
        access_token=token.get('access_token')
        refresh_token=token.get('refresh_token')

        if not access_token or not refresh_token:
            return Response(ApiResponse.error(401,"token not found",error="Unauthorized user").__dict__,status=401)

        refresh_token_data=jwt.decode(refresh_token,os.getenv('SECURE_KEY'),algorithms=["HS256"])
        user_id=refresh_token_data.get('id')

        if not user_id:
            return Response(ApiResponse.error(498,"token not found",error="Unauthorized user").__dict__,status=498)

        new_token=generated_refreshToken(user)

        return new_token
    except Exception as e:
        logger.debug(f"Error : {e}")


