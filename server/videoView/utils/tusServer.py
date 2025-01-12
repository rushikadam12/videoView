
# from tuspy.storage import FileSystemStorage
# from django.conf import settings
# import os
# from django.http import JsonResponse



# def tus_upload_server(request):
    
#     upload_dir=settings.UPLOAD_DIR

#     if not os.path.exists(upload_dir):
#         os.mkdir(upload_dir)
    
#     storage=FileSystemStorage(upload_dir)
#     handlers=TusHandler(storage=storage)
#     tus_server=TusServer(handlers)        

#     resp=tus_server.handler_request(request)
    
#     return resp




