from django.contrib import admin
from .models import Account
# Register your models here.
from import_export.admin import ImportExportModelAdmin
#admin.site.register(Account)

@admin.register(Account)

class ViewAdmin(ImportExportModelAdmin):
    pass

