from django.db import models
from .club import Club

# cached property
from django.utils.functional import cached_property


class Envoy(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="photos", null=True, blank=True)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    active = models.BooleanField(default=True)
    inactive_cause = models.CharField(max_length=255, null=True, blank=True)
    waiver_desc = models.TextField(null=True, blank=True)
    district_num = models.IntegerField()
    district_name = models.CharField(max_length=255)
    voivodeship = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="envoys")
    birth_date = models.DateField()
    birth_location = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255)
    number_of_votes = models.IntegerField()

    @cached_property
    def is_female(self) -> bool:
        return self.first_name.endswith("a")

    @cached_property
    def title(self) -> str:
        prefix = "Posłanka" if self.is_female else "Poseł"
        return f"{prefix} {self.first_name} {self.last_name}"

    def full_name(self) -> str:
        return f"{self.first_name} {self.second_name if self.second_name else ''} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.club.id})"
