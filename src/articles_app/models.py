from django.db import models
from sejm_app.models import Club, Envoy
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/")
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    envoys = models.ForeignKey(Envoy, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.title
