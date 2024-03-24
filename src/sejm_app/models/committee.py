from django.db import models
from .envoy import Envoy


class CommitteeType(models.TextChoices):
    EXTRAORDINARY = "EXTRAORDINARY", "Nadzwyczajna"
    INVESTIGATIVE = "INVESTIGATIVE", "Śledcza"
    STANDING = "STANDING", "Stała"


class Committee(models.Model):
    name = models.CharField(max_length=512)
    nameGenitive = models.CharField(max_length=512)
    code = models.CharField(max_length=10, unique=True)
    appointmentDate = models.DateField()
    compositionDate = models.DateField()
    phone = models.CharField(max_length=100, blank=True)
    scope = models.TextField(null=True)
    type = models.CharField(
        max_length=50, choices=CommitteeType.choices, default=CommitteeType.STANDING
    )

    def __str__(self):
        return self.name


class CommitteeMember(models.Model):
    committee = models.ForeignKey(
        Committee, related_name="members", on_delete=models.CASCADE
    )
    envoy = models.ForeignKey(Envoy, on_delete=models.CASCADE)
    function = models.CharField(
        max_length=100, blank=True, null=True
    )  # Function within the committee

    class Meta:
        unique_together = ("committee", "envoy")

    def __str__(self):
        return f"{self.envoy.full_name()} - {self.committee.name}"
