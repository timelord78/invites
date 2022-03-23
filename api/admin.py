from django.contrib import admin
from .models import CustomUser, Invitation


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone', 'invite_code',)


@admin.register(Invitation)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'invitee', 'inviter')
