from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.


class Task(models.Model):
    
    recipients = models.ManyToManyField(User, through='TaskUsers')
    title = models.CharField(max_length=150)
    content = models.TextField()
    start_date = models.DateField(default=timezone.now)
    deadline = models.DateField()
    location = models.CharField(max_length=100)

    class Meta:
        ordering = ["deadline"]
    
    def __str__(self):
        return self.title
    
    @property
    def task_creator(self):
        return self.taskusers_set.get(creator=True).user
    

class TaskUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    creator = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    revised = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    not_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["completed", "task__deadline"]

    def __str__(self):
        return self.task.title



class TaskHistory(models.Model):
    task = models.ForeignKey(TaskUsers, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_time_action = models.DateTimeField(auto_now_add=True)
    revised = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    reopen = models.BooleanField(default=False)

    class Meta:
        ordering = ["data_time_action"]

