from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt

from users.models import User
from django.shortcuts import render

import os
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, PasswordResetView
from django.contrib import messages
from django.utils.translation import gettext as _

import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomResetPasswordForm
from django.core.paginator import Paginator
from django.http import JsonResponse

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


def user_redirect(request):
    user = request.user
    if user.is_authenticated:
        user = request.user
        user_role = user.role
        # if user_role and user_role.slug == "nex-admin":
        #     return redirect("dashboard_view")
        #     # return redirect("users:account_login")
        # if user_role and user_role.slug == "client-admin":
        #     return redirect("dashboard_view")
        # if user_role and user_role.slug == "member":
        #     return redirect("dashboard_view")
        return redirect("users:home")
    else:
        return redirect("users:account_login")


# views.py


def is_ajax(request):
    # print("-------------------------------", request.META.get("HTTP_X_REQUESTED_WITH"))
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"



@login_required
def home_view(request):
    return render(request, "pages/home.html")






def logout_view(request):
    logout(request)
    return redirect("users:account_login")




class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, _("Given credentials are not valid"))
        return super().form_invalid(form)


class CustomForgotPasswordView(PasswordResetView):
    form_class = CustomResetPasswordForm
    template_name = "account/password_reset.html"
    success_url = "/accounts/password/reset/done/"





from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomChangePasswordForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomChangePasswordForm
    success_url = reverse_lazy("home")  
    template_name = "account/password_change.html" 

    def form_valid(self, form):
   
        result = super().form_valid(form)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Q

from django.contrib import messages
from .forms import *
from .models import *
import secrets
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            random_password = generate_random_password(length=10)
            user.set_password(random_password)
            
            user.save()
            print(f"Generated password for user {user.phone_number}: {random_password}")
            messages.success(request, 'User created successfully.')  
            return redirect('users:user_list')
        else:
            messages.error(request, 'Please correct the errors below.')  
            print(form.errors)
    else:
        form = UserForm()  

    return render(request, 'users/user_form.html', {'form': form})


def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.') 
            return redirect('users:user_list') 
        else:
            messages.error(request, 'Please correct the errors below.') 
    else:
        form = UserForm(instance=user) 

    return render(request, 'users/user_form.html', {'form': form})




def user_list(request):
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')

    users = User.objects.all()

    if search_query:
        if not search_query.isdigit():
            users = users.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        else:
            users = users.filter(
                Q(phone_number__icontains=search_query)
            )
    if role_filter:
        users = users.filter(role__role_name=role_filter)

    paginator = Paginator(users, 25)  # 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    roles = Role.objects.all()
    return render(request, 'users/user_list.html', {
        'page_obj': page_obj,
        'roles': roles,
        'search_query': search_query,
        'role_filter': role_filter,
        'title': "Users List",
    })

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})



def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User has been deleted successfully.")
        return redirect('users:user_list')  
    return redirect('users:user_list')





def status_view(request):
    return JsonResponse({"status": "OK"}, status=200)