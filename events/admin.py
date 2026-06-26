from django.contrib import admin
from .models import Event
# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event_type",
        "venue",
        "status",
        "start_datetime",
        "registration_deadline",
    )

    list_filter = (
        "status",
        "event_type",
        "organizer_clubs",
    )

    search_fields = (
        "title",
        "venue",
        "coordinator_name",
    )

    filter_horizontal = (
        "organizer_clubs",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-start_datetime",
    )