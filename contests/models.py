from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title