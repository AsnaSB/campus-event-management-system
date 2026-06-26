from django.contrib import admin
from django.utils.html import format_html

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    # ----------------------------------
    # List Page
    # ----------------------------------

    list_display = (
        "poster_preview",
        "title",
        "event_type",
        "venue",
        "status",
        "start_datetime",
        "published_by",
    )

    list_filter = (
        "status",
        "event_type",
        "organizer_clubs",
        "start_datetime",
    )

    search_fields = (
        "title",
        "venue",
        "coordinator_name",
        "coordinator_email",
    )

    ordering = (
        "-start_datetime",
    )

    date_hierarchy = "start_datetime"

    filter_horizontal = (
        "organizer_clubs",
    )

    readonly_fields = (
        "poster_preview",
        "created_at",
        "updated_at",
        "published_by",
    )

    # ----------------------------------
    # Form Layout
    # ----------------------------------

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "description",
                    "poster",
                    "poster_preview",
                )
            },
        ),

        (
            "Event Details",
            {
                "fields": (
                    "event_type",
                    "venue",
                    "start_datetime",
                    "end_datetime",
                    "status",
                )
            },
        ),

        (
            "Registration",
            {
                "fields": (
                    "registration_deadline",
                    "max_participants",
                    "registration_fee",
                )
            },
        ),

        (
            "Organizers",
            {
                "fields": (
                    "organizer_clubs",
                    "published_by",
                )
            },
        ),

        (
            "Coordinator",
            {
                "fields": (
                    "coordinator_name",
                    "coordinator_email",
                    "coordinator_phone",
                )
            },
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # ----------------------------------
    # Poster Preview
    # ----------------------------------

    def poster_preview(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;" />',
                obj.poster.url,
            )
        return "No Poster"

    poster_preview.short_description = "Poster"

    # ----------------------------------
    # Automatically Assign Publisher
    # ----------------------------------

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.published_by = request.user

        super().save_model(request, obj, form, change)