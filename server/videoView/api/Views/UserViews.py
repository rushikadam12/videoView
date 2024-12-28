import logging
from django.http import JsonResponse
from rest_framework.decorators import api_view

logger = logging.getLogger('api')  

@api_view(['GET'])
def index(request):
    
    return JsonResponse({"status":"ok"},status=200)

@api_view(['GET'])
def health_check(request):
    logger.debug("Health check endpoint accessed")
    data="hello from server"
    return JsonResponse({"data":data},status=200)