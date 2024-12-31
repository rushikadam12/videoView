import logging
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password

logger=logging.getLogger('api')

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