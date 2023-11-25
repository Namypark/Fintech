from django.contrib import admin
from .models import Account, KYC, CreditCard, Transaction
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Account)
class AccountAdminModel(ImportExportModelAdmin):
    model = Account
    list_editable = ["status", "account_balance"]
    list_display = ["user", "account_number", "account_balance", "status"]
    list_filter = ["status"]


@admin.register(KYC)
class KYCAdminModel(ImportExportModelAdmin):
    model = KYC
    search_fields = ["full_name"]
    list_display = ["user", "full_name", "gender", "country"]


@admin.register(Transaction)
class TransactionAdminModel(ImportExportModelAdmin):
    model = Transaction
    search_fields = ["transaction_id", "reference_number", "transaction_time"]
    list_display = [
        "transaction_id",
        "amount",
        "sender",
        "receiver",
        "status",
        "transaction_type",
        "transaction_description",
        "transaction_time",
        "transaction_fee",
    ]
    list_filter = [
        ("transaction_time", admin.DateFieldListFilter),
    ]
    date_hierarchy = "transaction_time"


@admin.register(CreditCard)
class CreditCardAdminModel(admin.ModelAdmin):
    model = CreditCard
    search_fields = ["cardholder_name", "card_number"]
    list_editable = ["card_type"]
    list_filter = [["date", admin.DateFieldListFilter]]
    list_display = ["user", "card_type", "cardholder_name", "date"]
    date_hierarchy = "date"
