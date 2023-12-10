from django.db import models
from .envoy import Envoy
from .club import Club


class ScandalEntryStatus(models.TextChoices):
    """Status of a scandal entry."""

    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class Scandal(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    envoys = models.ManyToManyField(Envoy, related_name="scandals", blank=True)
    clubs = models.ManyToManyField(Club, related_name="scandals", blank=True)
    entry_status = models.CharField(
        max_length=20,
        choices=ScandalEntryStatus.choices,
        default=ScandalEntryStatus.PENDING,
    )
    # get logged admin.user that created the scandal
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="scandals",
        help_text="Author of the description",
    )

    url1 = models.URLField(null=True, blank=True)
    url2 = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})"
