import logging
from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.serializer import UsersRegistrationSerializer
from api.models import Users
logger = logging.getLogger('api.UserViews')  


@api_view(['GET'])
def health_check(request):
    logger.debug("Health check endpoint accessed")
    return JsonResponse({"status":"ok"},status=200)


@api_view(['POST'])
def user_login(request):
    logger.debug("login view accessed")

    return JsonResponse({"status":"ok"},status=200)


@api_view(['POST'])
def signup(request):

    serializer=UsersRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user=serializer.save()
        print(serializer)
        return JsonResponse({"message":"saved successfully","data":serializer.data})
    return JsonResponse({"message":serializer.errors})