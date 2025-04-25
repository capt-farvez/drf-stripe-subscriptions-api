from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
)
from django.utils import timezone
import uuid

# Custom manager for User model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="Customer"):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        # Automatically add the user to the correct group based on their role
        if role == "admin":
            user.is_staff = True
            admin_group, _ = Group.objects.get_or_create(name="ADMIN")
            admin_group.user_set.add(user)  # Ensure user is the actual User instance
        else:
            customer_group, _ = Group.objects.get_or_create(name="CUSTOMER")
            customer_group.user_set.add(user)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password, role="admin")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    is_subscribed = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)  # Admin flag
    is_active = models.BooleanField(default=True)  # Active user flag
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.name
