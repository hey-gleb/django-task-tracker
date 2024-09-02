from django.contrib import admin

from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Task, TaskAdmin)
