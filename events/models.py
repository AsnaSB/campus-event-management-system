from django.db import models
from django.contrib.auth.models import User
from clubs.models import Club

from django.core.exceptions import ValidationError
from django.utils import timezone
import re

# Create your models here.
class EventType(models.TextChoices):
    WORKSHOP = "Workshop", "Workshop"
    SEMINAR = "Seminar", "Seminar"
    CONFERENCE = "Conference", "Conference"
    HACKATHON = "Hackathon", "Hackathon"
    COMPETITION = "Competition", "Competition"
    WEBINAR = "Webinar", "Webinar"
    BOOTCAMP = "Bootcamp", "Bootcamp"
    TECHNICAL_TALK = "Technical Talk", "Technical Talk"
    CULTURAL_EVENT = "Cultural Event", "Cultural Event"
    OTHER = "Other", "Other"


class EventStatus(models.TextChoices):
    DRAFT = "Draft", "Draft"
    PUBLISHED = "Published", "Published"
    REGISTRATION_OPEN = "Registration Open", "Registration Open"
    REGISTRATION_CLOSED = "Registration Closed", "Registration Closed"
    ONGOING = "Ongoing", "Ongoing"
    COMPLETED = "Completed", "Completed"
    CANCELLED = "Cancelled", "Cancelled"
    POSTPONED = "Postponed", "Postponed"
    ARCHIVED = "Archived", "Archived"


class Event(models.Model):
    """
    Stores details of events organized by one or more clubs.
    """

    # -------------------------
    # Basic Information
    # -------------------------

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    poster = models.ImageField(
        upload_to="event_posters/"
    )

    # -------------------------
    # Event Details
    # -------------------------

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices
    )

    venue = models.CharField(
        max_length=200
    )

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    # -------------------------
    # Registration Details
    # -------------------------

    registration_deadline = models.DateTimeField()

    max_participants = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    registration_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(0)
        ]
    )

    # -------------------------
    # Relationships
    # -------------------------

    organizer_clubs = models.ManyToManyField(
        Club,
        related_name="events"
    )

    published_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="published_events"
    )

    # -------------------------
    # Coordinator Details
    # -------------------------

    coordinator_name = models.CharField(
        max_length=100
    )

    coordinator_email = models.EmailField()

    coordinator_phone = models.CharField(
        max_length=15
    )

    # -------------------------
    # Event Status
    # -------------------------

    status = models.CharField(
        max_length=30,
        choices=EventStatus.choices,
        default=EventStatus.DRAFT
    )

    # -------------------------
    # Timestamps
    # -------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-start_datetime"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def clean(self):
        """
        Performs custom validation for the Event model.
        """

        errors = {}

        # End time must be after start time
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                errors["end_datetime"] = (
                    "The event end date and time must be after the start date and time."
                )

        # Registration deadline must be before or equal to event start
        if self.registration_deadline and self.start_datetime:
            if self.registration_deadline > self.start_datetime:
                errors["registration_deadline"] = (
                    "The registration deadline cannot be after the event start date and time."
                )

        # Registration deadline must not be after the event end
        if self.registration_deadline and self.end_datetime:
            if self.registration_deadline > self.end_datetime:
                errors["registration_deadline"] = (
                    "The registration deadline cannot be after the event end date and time."
                )

        # Validate coordinator phone number
        if self.coordinator_phone:
            phone_pattern = r"^[6-9]\d{9}$"

            if not re.match(phone_pattern, self.coordinator_phone):
                errors["coordinator_phone"] = (
                    "Enter a valid 10-digit Indian mobile number."
                )

        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        """
        Runs model validation before saving.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title