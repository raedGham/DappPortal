from django.contrib import admin
from .models import Position
# Register your models here.

class PosAdmin(admin.ModelAdmin):
    list_display = ('pos_name','description')


admin.site.register(Position,PosAdmin)