from django.contrib import admin

from .models import Task, TaskUsers, TaskHistory
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskUsers)
admin.site.register(TaskHistory)