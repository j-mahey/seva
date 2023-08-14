from django.contrib import admin

from .models import Movement


class MovementAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "in_time", "out_time", "vehicle", "note"]
    search_fields = ["user.badge"]
    ordering = ["date"]


admin.site.register(Movement, MovementAdmin)