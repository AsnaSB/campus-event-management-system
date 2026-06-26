from django.contrib import admin
from .models import Club
# Register your models here.
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display=("short_name","name","user","is_active",)
    search_fields=("name","short_name",)
    list_filter=("is_active",)
    ordering=("name",)