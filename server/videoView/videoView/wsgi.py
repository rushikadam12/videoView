"""
WSGI config for videoView project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoView.settings')

application = get_wsgi_application()

# dont forget to write this idea in notebook 'vertical ai like small ai apps which provide ai feature using open_api_key'