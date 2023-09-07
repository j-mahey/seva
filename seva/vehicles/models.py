from django.db import models


class Vehicle(models.Model):
    TYPE = [
        ("CR", "Car"),
        ("BS", "Bus"),
        ("AT", "Auto"),
        ("TP", "Tampo"),
        ("SC", "Scooter"),
        ("MC", "Motorcycle")
    ]
    type = models.CharField(max_length=3, choices=TYPE)
    custom_id = models.CharField(max_length=10, unique=True, null=True)
    vehicle_no = models.CharField(max_length=10, unique=True)
    person = models.ForeignKey("persons.Person", on_delete=models.CASCADE, null=True)

    def __str__(self):
       return self.vehicle_no