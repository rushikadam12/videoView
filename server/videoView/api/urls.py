from django.urls import path
from api.Views.UserViews import *

urlpatterns=[
    path("healthcheck",health_check,name="health_check")  
]