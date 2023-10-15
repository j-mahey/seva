from django.db import models

class Person(models.Model):
    GENDER = [
        ("M", "MALE"),
        ("F", "FEMALE"),
    ]
    badge = models.CharField(max_length=6)
    full_name = models.CharField(max_length=25, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    contact_number = models.CharField(max_length=10)
    active = models.BooleanField(default=True)

    type = models.ForeignKey('auth.Group', on_delete=models.CASCADE)
    centre = models.ForeignKey("centres.Centre", on_delete=models.CASCADE, null=True)
    department = models.ForeignKey("departments.Department", on_delete=models.CASCADE, null=True)

    centre_badge = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.badge

    def save(self, *args, **kwargs):
        # auto create badge for visitor or guest
        if self.type.name == "VISITOR":
            badge = 'V' + format(int(len(Person.objects.filter(type__name="VISITOR")) + 1), '05d')
            self.badge = badge
        if self.type.name == "GUEST":
            badge = 'G' + format(int(len(Person.objects.filter(type__name="GUEST")) + 1), '05d')
            self.badge = badge
        self.centre_badge = self.centre.code + self.badge

        for field_name in ['badge', 'full_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())

        super(Person, self).save(*args, **kwargs)
