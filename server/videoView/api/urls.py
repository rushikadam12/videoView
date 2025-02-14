from django.urls import path
from api.Views.UserViews import *
from api.Views.VideoView import *
from api.Views.SubscriberView import *
from api.Views.LikesView import *
from api.Views.CommentsView import *

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


    # subscriber
    path("toggle_subscription/<str:channel_id>/",toggle_subscription,name="toggle_subscription"),
    path("get_videos_by_channel_Id/<str:channel_id>/",get_videos_by_channel_Id,name="get_videos_by_channel_Id"),
    path("get_subscriber_count/<str:channel_id>/",get_subscriber_count,name="get_subscriber_count"),
    path("get_channel_info/<str:channel_id>/",get_channel_info,name="get_channel_info"),

    #Likes

    path("like_video_by_user/<str:video_id>/",like_video_by_user,name="like_video_by_user"),
    path("like_comment_by_user/<str:comment_id>/",like_comment_by_user,name="like_comment_by_user"),
    

    #Comments
    path("add_comment_to_video/<str:video_id>/",add_comment_to_video,name="add_comment_to_video"),
    path("delete_video_comment/<str:comment_id>/",delete_video_comment,name="delete_video_comment"),
    path("get_all_comments/<str:video_id>/",get_all_comments,name="get_all_comments"),
    
]