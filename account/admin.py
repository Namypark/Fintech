from django.contrib import admin
from .models import Account, KYC
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
