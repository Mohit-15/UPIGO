from django.contrib import admin
from .models import UPI

# Register your models here
@admin.register(UPI)
class UPIDetailAdmin(admin.ModelAdmin):
    list_display = ("username", "upi_id", "created_at", "updated_at")
    list_filter = ("username", "is_active")
    readonly_fields = ('created_at', 'updated_at',)

    fieldsets = (
        (None, {"fields": ("username", "upi_id", "upi_pin", "scan_code")}),
        ("Update Status", {"fields": ("created_at", "updated_at", )}),
        ("Activity Status", {"fields": ("is_active",)}),
    )
    search_fields = ("username", "is_active")
    ordering = ("username",)
    filter_horizontal = ()
