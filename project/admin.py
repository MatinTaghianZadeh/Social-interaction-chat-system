from django.contrib import admin
from project.models import UserProfile, GroupChat, Message, JoinRequest
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(GroupChat)
admin.site.register(Message)
admin.site.register(JoinRequest)


class JoinRequestAdmin(admin.ModelAdmin):
    list_display = {"user", "group", "status", "admin_approved"}
    list_filter = {"status", "admin_group"}

    actions = ["approve_selected", "reject_selected"]

    def approve_selected(self, request, queryset):
        queryset.update(status="approved", admin_approved=True)

    def reject_selected(self, request, queryset):
        queryset.update(status="rejected", admin_approved=False)

    approve_selected.short_description = "Approve selected join request"
    reject_selected.short_description = "Reject selected join request"