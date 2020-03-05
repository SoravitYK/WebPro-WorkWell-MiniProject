from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    money = models.IntegerField()

class TopupLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.IntegerField()
    topup_date = models.DateTimeField(auto_now=True)
    topup_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Zone(models.Model):
    zone = (
        ('GR', 'Green Zone'),
        ('GO', 'Gold Zone'),
        ('PR', 'Private Zone')
    )

    title = models.CharField(max_length=2, choices=zone)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()

class SeatBooking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null = True)
    total_price = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)