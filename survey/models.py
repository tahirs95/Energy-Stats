from django.db import models
from django.contrib.auth.models import User

class Use(models.Model):
    uses = models.CharField(max_length=50)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    building_name = models.CharField(max_length=50)
    address = models.TextField(default="Provide Description")
    square_footage = models.IntegerField()

    uses = models.ManyToManyField(Use)

    applicable_options = models.ManyToManyField(Option)

    electricity_provider = models.CharField(max_length=50)
    group = models.CharField(max_length=50)

    aggregated_bills = models.ManyToManyField(Bill)

    co2_current = models.FloatField()
    co2_2024 = models.FloatField()
    co2_2030 = models.FloatField()


    def __str__(self):
        return self.title


