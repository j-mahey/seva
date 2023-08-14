from django.db import models


class Centre(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=25, unique=True, blank=True, null=True)

    def __str__(self):
       return self.code