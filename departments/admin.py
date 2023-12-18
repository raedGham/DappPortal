from django.contrib import admin
from .models import Department
# Register your models here.

class DepAdmin(admin.ModelAdmin):
    list_display = ('name','description')


admin.site.register(Department,DepAdmin)