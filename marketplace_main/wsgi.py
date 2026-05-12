"""
WSGI config for marketplace_main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace_main.settings')

<<<<<<< HEAD
<<<<<<< HEAD
application = get_wsgi_application()
=======
application = get_wsgi_application()
>>>>>>> 0ace29bab589eee8093e09f15fbbd24c914a2197
=======
application = get_wsgi_application()
>>>>>>> origen/main
