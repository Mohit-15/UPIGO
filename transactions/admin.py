from django.contrib import admin
from .models import Transaction

# Register your models here
@admin.register(Transaction)
class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "user", "amount", "done_on", "is_credit", "not_pending")
    list_filter = ("user", "not_pending", "is_credit")
    readonly_fields = ('transaction_id', 'done_on',)

    fieldsets = (
        (None, {"fields": ("transaction_id", "user",)}),
        ("Transaction Details", {"fields": ("transfer_to", "received_from", "amount",)}),
        ("Transaction Status", {"fields": ("done_on", "not_pending",)}),
        ("Credit / Debit", {"fields": ("is_credit",)}),
    )
    search_fields = ("user", "transaction_id")
    filter_horizontal = ()
