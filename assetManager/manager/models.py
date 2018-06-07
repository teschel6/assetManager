from django.db import models
from django.utils import timezone

# Create your models here.
#models.DateField()
#models.PositiveIntegerField()
#models.CharField(max_length=N)

class Inventory(models.Model):
    asset_tag = models.PositiveIntegerField(primary_key=True) #Primary Key
    computer_name = models.CharField(max_length = 32)
    model = models.CharField(max_length = 64)
    os = models.CharField(max_length = 32)
    serial = models.CharField(max_length = 32)
    service_tag = models.CharField(max_length = 16)
    purchase_date = models.DateField()
    warrenty_expiration = models.DateField()
    last_update = models.DateField()
    notes = models.CharField(max_length = 256)

class Group(models.Model):
    group = models.CharField(primary_key=True,max_length=32)


class Deployed(models.Model):
    asset_tag = models.OneToOneField(
        Inventory,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    username = models.CharField(max_length = 32)
    location = models.CharField(max_length = 32)
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    date_issued = models.DateField()

class History(models.Model):
    asset_tag = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    username = models.CharField(max_length = 32)
    loaction = models.CharField(max_length = 32)
    date_issued = models.DateField()
    date_returned = models.DateField()



