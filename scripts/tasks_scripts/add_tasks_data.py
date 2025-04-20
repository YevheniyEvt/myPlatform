"""Add tasks app data to fill database"""
from django.db.models import F
from django.contrib.auth.models import User

from tasks.models import Task, TaskUsers
from tasks.utils import get_user_location, employee_tasks_allowed_locations, users_to_tasks_create
from scripts.tasks_scripts import data

COUNT_QUICK_TASKS = 15
COUNT_DISTRIBUTION_TASKS = 10
TASKS_COMPLETED = 5
TASKS_NOT_ACCEPTED = 5


TEXT = data.TEXT

def create_distribution_task():
    user = User.objects.get(username='admin')
    location = get_user_location(user)
    locations, _ = employee_tasks_allowed_locations(user)
    recipient = users_to_tasks_create(recipients_list=[recipient.id for recipient in locations],
                                      recipients_type=locations[0])
    for index in range(COUNT_DISTRIBUTION_TASKS):
        task = Task.objects.create(
            title=' '.join(TEXT[index:index + 4]),
            content=' '.join(TEXT[index:index + 10]),
            location=location,
            start_date='2025-04-07',
            deadline='2025-04-07'
        )
        task.recipients.set(recipient)
        task.recipients.add(user, through_defaults={"creator": True})

def create_quick_task():
    user = User.objects.get(username='admin')
    location = get_user_location(user)
    for index in range(COUNT_QUICK_TASKS):
        task = Task.objects.create(
            title=' '.join(TEXT[index:index + 4]),
            content=' '.join(TEXT[index:index + 10]),
            location=location,
            start_date='2025-04-07',
            deadline='2025-04-07'
        )
        task.recipients.add(user, through_defaults={"creator": True})

def create_completed_task():
    user = User.objects.get(username='admin')
    tasks = Task.objects.filter(taskusers__user=user)
    for task in tasks[:TASKS_COMPLETED]:
        TaskUsers.objects.filter(task=task, user=user).update(completed=~F("completed"))


def create_not_accepted_task():
    user = User.objects.get(username='admin')
    tasks = Task.objects.filter(taskusers__user=user)
    for task in tasks[TASKS_COMPLETED:TASKS_NOT_ACCEPTED + TASKS_COMPLETED]:
        TaskUsers.objects.filter(task=task, user=user).update(not_accepted=~F("not_accepted"))


def database_is_empty():
    return not Task.objects.first()

def tasks_run():
    if database_is_empty():
        print('Start create tasks data...', end=' ')
        create_quick_task()
        create_distribution_task()
        create_completed_task()
        create_not_accepted_task()
        print('Ok')
    else:
        print('Tasks data - Ok')
