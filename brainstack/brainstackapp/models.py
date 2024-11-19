from django.db import models

# Create your models here.

class AirPollution(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    pm =  models.CharField(max_length=10)
    dewp = models.IntegerField()
    temp = models.IntegerField()
    pres = models.IntegerField()
    cbwd = models.CharField(max_length=10)
    lws = models.FloatField()
    ls = models.CharField(max_length=2)
    lr =  models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.year}"
