from django.contrib import admin
from .models import Position
from import_export.admin import ImportExportModelAdmin
# Register your models here.

# class PosAdmin(admin.ModelAdmin):
#     list_display = ('title','description')


# admin.site.register(Position,PosAdmin)

@admin.register(Position)

class ViewAdmin(ImportExportModelAdmin):
    pass
