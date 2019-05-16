from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import PlatformUser
from .forms import PlatformUserChangeForm, PlatformUserCreationForm


class PlatformUserAdminForm(UserAdmin):
    add_form = PlatformUserCreationForm
    form = PlatformUserChangeForm
    model = PlatformUser

    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin', )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    filter_horizontal = ()


admin.site.register(PlatformUser, PlatformUserAdminForm)
admin.site.unregister(Group)

