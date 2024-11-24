from django.contrib import admin

from user.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar', 'phone_number', 'country')
    list_filter = ('country',)
    search_fields = ('country', 'email')