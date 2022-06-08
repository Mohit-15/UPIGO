from django.contrib.auth.models import BaseUserManager
from rest_framework import authentication


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, mobile_no=None, role=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")

        user = self.model(
            email=self.normalize_email(email), name=name, mobile_no=mobile_no
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile_no=None, password=None):
        user = self.create_user(
            email, password=password, name=name, mobile_no=mobile_no
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class TokenAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
