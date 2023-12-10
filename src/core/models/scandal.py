from django.db import models
from .envoy import Envoy
from .club import Club


class Scandal(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    envoys = models.ManyToManyField(Envoy, related_name="scandals", blank=True)
    clubs = models.ManyToManyField(Club, related_name="scandals", blank=True)
    url1 = models.URLField(null=True, blank=True)
    url2 = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})"
