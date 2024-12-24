# models.py
from django.db import models
from django.utils.timezone import now
from config.settings.middleware import get_current_user
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        "User", related_name="created_%(class)s_set", null=True, blank=True, on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        "User", related_name="updated_%(class)s_set", null=True, blank=True, on_delete=models.SET_NULL
    )
    deleted_by = models.ForeignKey(
        "User", related_name="deleted_%(class)s_set", null=True, blank=True, on_delete=models.SET_NULL
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not self.pk:
            self.created_by = user
        elif user:
            self.updated_by = user
        super().save(*args, **kwargs)

    def soft_delete(self):
        user = get_current_user()
        self.is_deleted = True
        self.deleted_at = now()
        if user:
            self.deleted_by = user
        self.save()

class Role(BaseModel):
    role_name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.role_name

class UserManager(BaseUserManager):
    def _create_user(self, email, phone_number, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        monitor_role, _ = Role.objects.get_or_create(role_name="monitor")
        extra_fields.setdefault("role", monitor_role)
        return self._create_user(email, phone_number, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.BigIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1000000000, message="Phone number must be at least 10 digits."),
            MaxValueValidator(9999999999, message="Phone number cannot exceed 10 digits."),
        ],
    )
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.id})

    def clean(self):
        super().clean()
        if len(str(self.phone_number)) != 10:
            raise ValidationError({"phone_number": "Phone number must contain exactly 10 digits."})
