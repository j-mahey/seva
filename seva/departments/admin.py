from django.contrib import admin

from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


admin.site.register(Department, DepartmentAdmin)