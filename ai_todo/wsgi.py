"""
WSGI config for ai_todo project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_todo.settings')

application = get_wsgi_application()
