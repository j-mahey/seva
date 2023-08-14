from django.db import models


class Vehicle(models.Model):
    TYPE = [
        ("CR", "Car"),
        ("TP", "Tempo"),
        ("SC", "Scooter"),
        ("MC", "Motorcycle")
    ]
    type = models.CharField(max_length=3, choices=TYPE)
    custom_id = models.CharField(max_length=10, unique=True, null=True)
    vehicle_no = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)

    def __str__(self):
       return self.vehicle_no