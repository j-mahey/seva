from django import forms
from django.contrib import admin

from persons.models import Person
from centres.models import Centre


class StaffCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["badge", "full_name", "gender", "contact_number", "centre", "department"]
        

class VisitorCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["full_name", "gender", "contact_number", "centre", "department"]


class GuestCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["full_name", "gender", "contact_number", "centre", "department"]


class PersonAdmin(admin.ModelAdmin):
    add_form = StaffCreationForm

    list_display = ["badge", "centre", "type", "full_name", "gender", "contact_number", "department"]
    search_fields = ["badge"]
    ordering = ["badge"]


admin.site.register(Person, PersonAdmin)