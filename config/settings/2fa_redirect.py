from django.conf import settings
from django.urls import reverse


class DynamicLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        home = reverse('home')

        if "allauth_2fa_user_id" in request.session:
            allauth_2fa_login = request.session.get("allauth_2fa_login", {})
            if allauth_2fa_login:
                allauth_2fa_login.update({"redirect_url": home})
                request.session["allauth_2fa_login"] = allauth_2fa_login

        return response
