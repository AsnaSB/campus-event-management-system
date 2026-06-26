from django.db import models
from django.contrib.auth.models import User
from clubs.models import Club

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

    def __str__(self):
        return self.title