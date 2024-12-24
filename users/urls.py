from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import *
# from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.urls import reverse_lazy

app_name = "users"
urlpatterns = [
    
    path('user/create/', create_user, name='create_user'),

    path('user/<int:user_id>/update/', update_user, name='update_user'),

    path('user/<int:pk>/', user_detail, name='user_detail'),

    path('user/list/', user_list, name='user_list'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    
    path("~redirect/", user_redirect, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),

    path("logout/", logout_view, name="account_logout"),
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path('accounts/signup/', RedirectView.as_view(url=reverse_lazy('account_login')), name='account_signup'),
    path(
        "forgot-password/",
        CustomForgotPasswordView.as_view(),
        name="account_reset_password",
    ),
    path('change-passord/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('status/', status_view, name='status'),
]