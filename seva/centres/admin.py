from django.contrib import admin

from .models import Centre


class CentreAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    search_fields = ["code"]
    ordering = ["code"]


admin.site.register(Centre, CentreAdmin)