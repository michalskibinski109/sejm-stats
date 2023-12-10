from django.db import models


class Club(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    members_count = models.IntegerField()
    photo = models.ImageField(upload_to="photos", null=True, blank=True)
