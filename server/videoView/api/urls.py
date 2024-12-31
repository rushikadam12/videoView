from django.urls import path
from api.Views.UserViews import *

urlpatterns=[

    path("healthcheck",health_check,name="health_check"),
    # users
    path("signup",signup,name="signup") ,
    path("login",login,name="login")  ,
    path("getuser",get_user,name="getuser")  ,
    path("logout",logout_user,name="logout_user"),
    path("update_user",update_user,name="update_user") ,
    path("generate_new_token",request_access_token,name="request_access_token"),
    path("reset_password",reset_password,name="reset_password") 

]