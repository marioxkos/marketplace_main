"""
ASGI config for marketplace_main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace_main.settings')

<<<<<<< HEAD
<<<<<<< HEAD
application = get_asgi_application()
=======
application = get_asgi_application()
>>>>>>> 0ace29bab589eee8093e09f15fbbd24c914a2197
=======
application = get_asgi_application()
>>>>>>> origen/main
