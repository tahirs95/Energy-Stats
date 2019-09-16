from django.db import models
from django.contrib.auth.models import User

class Use(models.Model):
    uses = models.CharField(max_length=50)
    use_num = models.IntegerField(default=1)

    def __str__(self):
        return self.uses

class Option(models.Model):
    options = models.CharField(max_length=50)

    def __str__(self):
        return self.options

class Bill(models.Model):
    bills = models.FloatField(max_length=50)

    def __str__(self):
        return str(self.bills)

class Building(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    title = models.CharField(max_length=20, null=True, blank=True)
    building_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(default="Provide Description", null=True, blank=True)
    square_footage = models.IntegerField(null=True, blank=True)
    uses = models.ManyToManyField(Use, blank=True)
    applicable_options = models.ManyToManyField(Option, blank=True)
    electricity_provider = models.CharField(max_length=50, null=True, blank=True)
    group = models.CharField(max_length=50, null=True, blank=True)
    aggregated_bills = models.ManyToManyField(Bill, blank=True)
    co2_current = models.FloatField(null=True, blank=True)
    co2_2024 = models.FloatField(null=True, blank=True)
    co2_2030 = models.FloatField(null=True, blank=True)
    page = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.title


