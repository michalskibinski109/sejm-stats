from django.db import models


# Create your models here.
class Publisher(models.Model):
    actsCount = models.IntegerField()
    code = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    shortName = models.CharField(max_length=255)
    years = models.JSONField()

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Reference(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# keywords
# ["Afganistan","Agencja Badań Medycznych","Agencja Bezpieczeństwa Wewnętrznego","Agencja Mienia Wojskowego","Agencja Nieruchomości Rolnych","Agencja Oceny Technologii Medycznych","Agencja Restrukturyzacji i Modernizacji Rolnictwa","Agencja Rezerw Materiałowych","Agencja Rezerw Strategicznych","Agencja Rozwoju Przemysłu S.A.","Agencja Rynku Rolnego","Agencja Wywiadu","Agencja Własności Rolnej Skarbu Państwa","Akademia Kopernikańska","Akademia Obrony Narodowej","Akademia Sztuki Wojennej","Albania","Algieria","Andora","Angol
