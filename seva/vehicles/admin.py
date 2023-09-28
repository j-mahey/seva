from django.contrib import admin
from django import forms

from .models import Vehicle
from centres.models import Centre
from persons.models import Person


class VehicleCreationForm(forms.ModelForm):

    centre = forms.ChoiceField(choices=[(x.code, x.code) for x in Centre.objects.all()], widget=forms.Select)
    badge = forms.CharField()
    class Meta:
        model = Vehicle
        fields = ["vehicle_no", "type",]


class VehicleAdmin(admin.ModelAdmin):
    add_from = VehicleCreationForm

    list_display = ["vehicle_no", "custom_id", "type", "person"]
    search_fields = ["vehicle_no", "custom_id"]
    ordering = ["vehicle_no"]


admin.site.register(Vehicle, VehicleAdmin)