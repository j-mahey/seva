from django import forms
from django.contrib import admin

from persons.models import Person
from centres.models import Centre


class PersonCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["type", "centre", "badge", "full_name", "gender", "contact_number", "department"]


class PersonAdmin(admin.ModelAdmin):
    add_form = PersonCreationForm

    list_display = ["badge", "centre", "type", "full_name", "gender", "contact_number", "department"]
    search_fields = ["badge"]
    ordering = ["badge"]


admin.site.register(Person, PersonAdmin)