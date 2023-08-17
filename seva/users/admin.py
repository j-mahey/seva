from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["badge", "full_name", "gender", "contact_number", "centre", "department"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class NormUserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["badge", "full_name", "gender", "contact_number", "centre", "department"]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["badge", "password", "full_name",
                  "gender", "contact_number", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["badge", "full_name", "gender", "contact_number", "centre", "department", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None,            {"fields": ["badge", "centre", "department", "password"]}),
        ("Personal info", {"fields": ["full_name", "gender", "contact_number"]}),
        ("Permissions",   {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["badge", "centre", "department", "full_name", "gender",
                           "contact_number", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["badge"]
    ordering = ["badge"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)