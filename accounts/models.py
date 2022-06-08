from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyUserManager
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .token import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.models import Site
from django.utils import timezone

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=40)
    mobile_validator = RegexValidator(
        regex=r"^\+?1?\d{9,14}$",
        message="Phone number must be entered in the format: '+9999999999'. Upto 14 digits allowed",
    )
    mobile_no = models.CharField(
        validators=[mobile_validator], max_length=15, unique=True
    )
    mobile_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "mobile_no"
    REQUIRED_FIELDS = ["name", "email"]

    def __str__(self):
        return self.mobile_no

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserDetail(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Trans-gender", "Trans-gender"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=50, blank=True, null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        name = instance.name if instance.name else "No name given"
        domain = "http://127.0.0.1:8000"
        subject = "[IMP] Account Verification: {}".format(name)
        message = render_to_string(
            "account/account_activation.html",
            {
                "user": instance,
                "domain": domain,
                "uid": urlsafe_base64_encode(force_bytes(instance.id)),
                "token": account_activation_token.make_token(instance),
            },
        )
        send_mail(
            subject,
            message,
            "msbproject1234@gmail.com",
            [instance.email],
            fail_silently=False,
        )
