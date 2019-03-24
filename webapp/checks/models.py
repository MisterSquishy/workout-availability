from django.db import models

# Create your models here.
class Check(models.Model):
    venue = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    slot_time = models.DateTimeField()
    open_seats = models.IntegerField()
    taken_seats = models.IntegerField()
    is_full = models.BooleanField(default=False)