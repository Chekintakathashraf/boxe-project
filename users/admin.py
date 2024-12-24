# from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import (
    User,Role
)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email","phone_number", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "role",
                   
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [ "id","name", "email","phone_number","role", "is_superuser"]
    search_fields = ["name","email","phone_number",]
    ordering = ["id"]
    list_filter = (
       "is_superuser",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email","phone_numer", "password1", "password2"),
            },
        ),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('role_name',)
    list_filter = ('is_deleted',)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()



# @admin.register(UsersModulesPrivileges)
# class UsersModulesPrivilegesAdmin(admin.ModelAdmin):

#     search_fields = (
#         "privilege",
#         "status_id",
#     )
#     list_display_links = ("id", "privilege")
#     list_display = (
#         "id",
#         "privilege",
#         "module_id",
#         "status_id",
#         "created_by",
#         "modified_by",
#         "created",
#         "modified",
#     )
#     list_filter = (
#         "privilege",
#         "status_id",
#         "created_by",
#         "modified_by",
#     )
#     ordering = ("created",)