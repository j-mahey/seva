from django.contrib import admin
from django import forms

from .models import Vehicle


class VehicleCreationForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ["vehicle_no", "custom_id", "type", "user"]


class VehicleAdmin(admin.ModelAdmin):
    add_from = VehicleCreationForm

    list_display = ["vehicle_no", "custom_id", "type", "user"]
    search_fields = ["vehicle_no", "custom_id"]
    ordering = ["vehicle_no"]


admin.site.register(Vehicle, VehicleAdmin)