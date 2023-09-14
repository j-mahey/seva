from django.contrib import admin
from django import forms

from .models import Movement


class MovementAdmin(admin.ModelAdmin):
    list_display = ["person", "date", "in_time", "out_time", "vehicle", "note"]
    search_fields = ["person.badge"]
    ordering = ["date"]


class MovementFilterForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ["person", "date", "vehicle"]


admin.site.register(Movement, MovementAdmin)