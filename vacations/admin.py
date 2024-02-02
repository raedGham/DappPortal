from django.contrib import admin
from .models import Vacation, EmployeeLeaveStat
#from import_export.admin import ImportExportModelAdmin

# Register your models here.

class VacAdmin(admin.ModelAdmin):
    list_display = ('vac_date','employee','from_date','to_date','nodays','ampm','first_approval', 'first_app_status','first_app_date')


admin.site.register(Vacation, VacAdmin)
admin.site.register(EmployeeLeaveStat)
