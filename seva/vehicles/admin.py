from django.contrib import admin

from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ["vehicle_no", "custom_id", "type", "user"]
    search_fields = ["vehicle_no", "custom_id"]
    ordering = ["vehicle_no"]


admin.site.register(Vehicle, VehicleAdmin)