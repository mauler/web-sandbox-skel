from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class Team(models.Model):
    name = models.CharField(max_length=200)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    team = models.ForeignKey("Team", null=True, blank=True,
                             related_name="members")

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
