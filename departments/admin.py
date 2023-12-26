from django.contrib import admin
from .models import Department
from import_export.admin import ImportExportModelAdmin

# Register your models here.

# class DepAdmin(admin.ModelAdmin):
#     list_display = ('name','description')


# admin.site.register(Department,DepAdmin)

@admin.register(Department)

class ViewAdmin(ImportExportModelAdmin):
    pass