from django.contrib import admin
from .models import Vacation
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class VacAdmin(admin.ModelAdmin):
    list_display = ('vac_date','employee','from_date','to_date','nodays','ampm')


# admin.site.register(Department,DepAdmin)

@admin.register(Vacation)

class ViewAdmin(ImportExportModelAdmin):
    pass