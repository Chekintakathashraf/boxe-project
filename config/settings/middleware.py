from django.shortcuts import redirect
from django.conf import settings

class RedirectAfter2FACompletedMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        response = self.get_response(request)
        
        if request.path == '/two-factor-authenticate/' and request.user.is_authenticated:
            if request.user.is_2fa_verified:
                return redirect(settings.LOGIN_REDIRECT_URL)
        
        return response
    
from allauth_2fa.middleware import BaseRequire2FAMiddleware
from django.conf import settings
 
 
class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        # Except Superusers all other users are require to have 2FA.
        if settings.REQUIRE_TWO_FACTOR_AUTH:
            return not request.user.is_superuser
        return False
    

import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, "user", None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = request.user
        response = self.get_response(request)
        return response
