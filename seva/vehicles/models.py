from django.db import models


class Vehicle(models.Model):
    TYPE = [
        ("CR", "CAR"),
        ("BS", "BUS"),
        ("AT", "AUTO"),
        ("TP", "TAMPO"),
        ("SC", "SCOOTER"),
        ("MC", "MOTORCYCLE")
    ]
    type = models.CharField(max_length=3, choices=TYPE)
    custom_id = models.CharField(max_length=10, unique=True, null=True)
    vehicle_no = models.CharField(max_length=10, unique=True)
    person = models.ForeignKey("persons.Person", on_delete=models.CASCADE, null=True)

    def __str__(self):
       return self.vehicle_no
    
    def save(self, *args, **kwargs):
        self.custom_id = str(len(Vehicle.objects.all()) + 1)

        for field_name in ['custom_id', 'vehicle_no']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())

        super(Vehicle, self).save(*args, **kwargs)
