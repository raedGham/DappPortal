from django.contrib import admin
from .models import Account
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from guardian.admin import GuardedModelAdmin

class AccountAdmin(GuardedModelAdmin):
    pass
admin.site.register(Account, UserAdmin)


# @admin.register(Account)
class ViewAdmin(ImportExportModelAdmin):
    pass



