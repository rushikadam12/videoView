from rest_framework.response import Response

class ApiResponse(Response):
    def __init__(self,status=500,message="",response=[],error=None):
        self.status=status
        self.message=message
        self.response=response
        self.error=error
    
    @staticmethod
    def success(status,message,response):
        return ApiResponse(status,message,response)
    
    @staticmethod
    def error(status,message,error):
        return ApiResponse(status,message,error)