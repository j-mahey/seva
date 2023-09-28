from django.db import models

class Person(models.Model):
    GENDER = [
        ("M", "Male"),
        ("F", "Female"),
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
        if self.type.name == "Visitor":
            badge = 'v' + format(int(len(Person.objects.filter(type__name="Visitor")) + 1), '05d')
            self.badge = badge
        if self.type.name == "Guest":
            badge = 'g' + format(int(len(Person.objects.filter(type__name="Guest")) + 1), '05d')
            self.badge = badge
        self.centre_badge = self.centre.code + self.badge
        super(Person, self).save(*args, **kwargs)