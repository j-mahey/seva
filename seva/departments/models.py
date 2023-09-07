from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=24, unique=True, blank=False)

    def __str__(self):
       return self.name.title()
