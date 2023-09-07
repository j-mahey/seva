from django.db import models
from django.utils import timezone


class Movement(models.Model):
    
    date = models.DateField()
    in_time = models.DateTimeField()
    out_time = models.DateTimeField(blank=True, null=True)
    person = models.ForeignKey("persons.Person", on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, null=True)
    note = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
       return self.person.badge
    
    def save(self, *args, **kwargs):
        self.date = timezone.now()
        self.in_time = timezone.now()
        return super(Movement, self).save(*args, **kwargs)
