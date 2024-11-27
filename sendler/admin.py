from django.contrib import admin

from sendler.models import Recipient, Message, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")
    search_fields = ("full_name", "email")
    ordering = ("full_name",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    search_fields = ("subject",)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status")
    list_filter = ("status",)
    search_fields = ("id",)