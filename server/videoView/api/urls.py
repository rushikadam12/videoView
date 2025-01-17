from django.urls import path
from api.Views.UserViews import *
from api.Views.VideoView import *

urlpatterns=[

    path("healthcheck",health_check,name="health_check"),
    # users
    path("signup",signup,name="signup") ,
    path("login",login,name="login")  ,
    path("getuser",get_user,name="getuser")  ,
    path("logout",logout_user,name="logout_user"),
    path("update_user",update_user,name="update_user") ,
    path("generate_new_token",request_access_token,name="request_access_token"),
    path("reset_password",reset_password,name="reset_password"),

    # video
    path("upload_video",upload_video,name="upload_user"),
    path("get_all_videos",get_all_videos,name="get_all_videos"),
    path("get_video_by_videoId/<str:id>/",get_video_by_videoId,name="get_video_by_videoId"),
    path("update_video/<str:id>/",update_video,name="update_video"),
    path("delete_video/<str:video_id>/",delete_video,name="delete_video"),
    path("is_published/<str:video_id>/",is_published,name="is_published"),


]