from .base import *
from config.env import *
DEBUG = env.bool('DJANGO_DEBUG',default=True)
 
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS',default=['*']) 