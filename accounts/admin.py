from django.contrib import admin
from .models import User, UserDetail
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "name", "mobile_no")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserDetail
        fields = (
            "user",
            "password",
            "gender",
            "age",
            "date_of_birth",
            "address",
            "aadhar_number",
            "pan_card",
            "account_balance",
        )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "name", "mobile_no", "mobile_verified")
    list_filter = ("email", "mobile_no")
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Personal Information", {"fields": ("mobile_no", "mobile_verified",)}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "mobile_no",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "name", "mobile_no")
    ordering = ("email",)
    filter_horizontal = ()


class UserDetailAdmin(BaseUserAdmin):
    model = UserDetail

    list_display = ("user", "age", "aadhar_number", "pan_card", "account_balance")
    list_filter = ("user", "gender")
    fieldsets = (
        (None, {"fields": ("user",)}),
        ("Personal Information", {"fields": ("age", "gender", "date_of_birth", "address",)}),
        ("Identity Details", {"fields": ("aadhar_number", "pan_card",)}),
        ("Account Details", {"fields": ("account_balance",)})
    )
    search_fields = ("user",)
    ordering = ("user",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserDetail, UserDetailAdmin)