from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, badge, full_name,
                    gender, contact_number, password=None):
        
        if not badge:
            raise ValueError("Users must have an badge number")

        user = self.model(
            badge=badge,
            full_name=full_name,
            gender=gender,
            contact_number=contact_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, badge, full_name,
                         gender, contact_number, password=None):
        
        user = self.create_user(
            badge,
            password=password,
            full_name=full_name,
            gender=gender,
            contact_number=contact_number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    ]
    badge = models.CharField(max_length=6, unique=True)
    full_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=1, choices=GENDER)
    contact_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    centre = models.ForeignKey("centres.Centre", on_delete=models.CASCADE, null=True)
    department = models.ForeignKey("departments.Department", on_delete=models.CASCADE, null=True)

    objects = UserManager()

    USERNAME_FIELD = "badge"
    REQUIRED_FIELDS = ["full_name", "gender", "contact_number"]

    def __str__(self):
        return self.badge

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin