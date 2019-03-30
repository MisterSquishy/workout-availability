from django.db import models

# Create your models here.
class Check(models.Model):
    venue = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    location_id = models.CharField(max_length=255, default="", db_index=True)
    location = models.CharField(max_length=255, db_index=True)
    slot_time = models.DateTimeField()
    open_seats = models.IntegerField(default=-1)
    taken_seats = models.IntegerField(default=-1)
    is_full = models.BooleanField(default=False)