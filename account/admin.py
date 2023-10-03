from django.contrib import admin
from .models import Account
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class AccountAdminModel(ImportExportModelAdmin):
    model = Account
    list_editable = ["status", "account_balance"]
    list_display = ["user", "account_number", "account_balance", "status"]
    list_filter = ["status"]


admin.site.register(Account, AccountAdminModel)
