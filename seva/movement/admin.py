from django.contrib import admin

from .models import Movement


class MovementAdmin(admin.ModelAdmin):
    list_display = ["person", "date", "in_time", "out_time", "vehicle", "note"]
    search_fields = ["person.badge"]
    ordering = ["date"]


admin.site.register(Movement, MovementAdmin)