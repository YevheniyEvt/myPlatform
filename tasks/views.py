import datetime

from django.db.models import F, Q, Count, Subquery, OuterRef, Sum, DecimalField, FloatField, ExpressionWrapper, Case, When, Value
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import AnonymousUser

from django.views.generic import View, ListView, DeleteView, UpdateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import BaseCreateView
from django.contrib.auth.models import User

from comunication.models import Coment, DeleteHistory
from comunication.utils import create_coment
from comunication.forms import ComentForm

from employee.models import StoreEmployee, RetailEmployee, OfficeEmployee
from employee.utils import get_user_location, get_management_positions, get_user_employee

from tasks.forms import TaskForm
from tasks.models import Task, TaskUsers, TaskHistory
from tasks.utils import employee_tasks_allowed_locations, users_to_tasks_create, get_users_from_location


# Create your views here.

class CreateTaskView(LoginRequiredMixin, BaseCreateView, ListView):
    model = Task
    form_class = TaskForm
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks:create_task')
    template_name = 'tasks/create_task.html'
    
    def setup(self, request, *args, **kwargs):
        try:
            self.recipients_query, self.recipients_type = employee_tasks_allowed_locations(request.user)
        except TypeError:
            pass
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients'] = self.recipients_query
        context['recipients_type'] = self.recipients_type
        context['positions'] = get_management_positions()
        return context
    
    def get_queryset(self):
        query  =super().get_queryset()
        return (query.
                annotate(task_count=Count('taskusers')).
                filter(taskusers__user=self.request.user).
                annotate(is_creator=Q(taskusers__creator=True))
                )
    
    def form_valid(self, form):
        response = super().form_valid(form)
        recipients_id_from_form = self.request.POST.getlist("recipients")
        users = users_to_tasks_create(recipients_list=recipients_id_from_form, recipients_type=self.recipients_type[0])
        self.object.recipients.set(users)
        self.object.recipients.add(self.request.user, through_defaults={"creator": True})
        return response

    
class MyTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        query = super().get_queryset()
        outeref_taskusers = TaskUsers.objects.filter(
             task=OuterRef('pk'),
             user=self.request.user
             )
        query = (query.
                filter(taskusers__user=self.request.user).
                annotate(
                    revised=Subquery(outeref_taskusers.values('revised')[:1]),
                    completed=Subquery(outeref_taskusers.values('completed')[:1]),
                    not_accepted=Subquery(outeref_taskusers.values('not_accepted')[:1]),
                    is_creator=Subquery(outeref_taskusers.values('creator')[:1]),
                    ))
        
        url = self.request.get_full_path()
        if reverse('tasks:my_tasks') == url:
            return query
        elif reverse('tasks:my_active_task') == url:
            return query.exclude(Q(completed=True) | Q(not_accepted=True)) 
        elif reverse('tasks:my_completed_task') == url:
            return query.filter(Q(completed=True) | Q(not_accepted=True))
        

class MyLocationTaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list_my_location_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        current_user_location = get_user_location(self.request.user)
        my_location_users = get_users_from_location(recipients_id=[current_user_location.id], recipients=current_user_location)
        query = super().get_queryset()
        percent_completed = Case(
            When(total=0, then=Value(0)),
            default=ExpressionWrapper(F('count_completed')*100/F('total'), output_field=DecimalField()
                                      ), output_field=DecimalField())
        query = (query.
                 filter(taskusers__user__in=my_location_users).
                 annotate(
                      count_completed=Count("taskusers", filter=Q(taskusers__completed=True)),
                      total=Count("taskusers", filter=Q(taskusers__creator=False)),
                      percent_completed=percent_completed, 
                      ))
        return query


class LocationTaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail_location_task.html"
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_location = get_user_location(self.request.user)
        my_location_users = get_users_from_location(recipients_id=[current_user_location.id], recipients=current_user_location)
        tasks_users = self.get_object().taskusers_set.filter(user__in=my_location_users)
        context['tasks_users'] = tasks_users
        return context


class MyTaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail_task.html'
    context_object_name = 'task'

    def get_object(self, queryset = ...):
        obj_query = super().get_object(queryset)
        obj_query = (obj_query.annotate(task_count=Count('taskusers')).
                 filter(
                     Q(task_count=1),Q(id=self.kwargs.get('pk')),
                     Q(taskusers__user=self.request.user)
                     ).first())
        return obj_query


    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if task is not None:
            TaskHistory.objects.get_or_create(
                user=self.request.user,
                task=self.get_object(),
                revised=True,
            )
            task_user = task.taskusers_set.filter(user=self.request.user).first()
            task_user.revised = timezone.now()
            task_user.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Coment.objects.filter(task=self.object)
        context['comments'] = comments
        return context
    
class CreateCommentView(CreateView):
    model = Task
    form_class = ComentForm
    
    def get_success_url(self):
        return reverse_lazy("tasks:detail_task", kwargs={'pk': self.task.id})
    
    def form_valid(self, form):
        self.task = self.get_object()
        form.instance.task = self.task 
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class DetailTaskCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        view = CreateCommentView.as_view()
        return view(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        view = MyTaskDetailView.as_view()
        return view(request, *args, **kwargs)
    


def detail_task(request, task_id):
    template_name = 'tasks/detail_task.html'
    date = timezone.localdate()
    current_user = get_user(request)

    
    task_current_user = TaskUsers.objects.get(id=task_id)
    task_history = TaskHistory.objects.filter(task=task_current_user)
    task = task_current_user.task
    if task_current_user is not None and request.method == 'GET' and task_current_user.revised is None:
        task_current_user.revised = timezone.now()
        task_current_user.save()
    
    my_personal_task = Task.objects.annotate(task_count=Count('taskusers')).filter(
        Q(task_count=1),
        Q(id=task_id),
        Q(taskusers__user=current_user),
        ).first()
    coments = Coment.objects.filter(task=task)
    
    context = {
        "task_current_user": task_current_user,
        "date": date,
        "object": task_current_user,
        "my_personal_task": my_personal_task,
        "coments": coments,
        "current_user": current_user,
        "task_history": task_history,

    }

    if request.method == "GET":
        TaskHistory.objects.get_or_create(
            user=current_user,
            task=task_current_user,
            revised=True
        )

    if request.method == "POST":
            if request.POST.get("content") is not None:
                create_coment(request=request, object=task) 
                return redirect("tasks:detail_task", task_id=task_id)

            
    return render(request, template_name, context)


def update_task(request, task_id):
        task_user_data = TaskUsers.objects.filter(id=task_id).first()
        task_data = Task.objects.filter(id=task_user_data.task.id)
        if request.method == 'POST':
            form = TaskForm(request.POST, initial=task_data.values()[0])
            if not form.has_changed():
                return redirect("tasks:detail_task", task_id=task_id)
            elif form.is_valid():
                form_data = form.cleaned_data
                updated_field = {field: form_data[field] for field in form.changed_data}
                Task.objects.filter(id=task_user_data.task.id).update(**updated_field)
                return redirect("tasks:detail_task", task_id=task_id)
        return redirect('tasks:my_active_task')

def delete_task(request, task_id):
    current_user = get_user(request)
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        content = f"user: {current_user}, delete task: {task.title}, with content:{task.content[:50]}."
        DeleteHistory.objects.create(user=current_user, content=content, task=True)
        Task.objects.get(id=task_id).delete()
        return redirect('tasks:my_active_task')

def complete_task(request, task_id):
        task = TaskUsers.objects.get(id=task_id)
        current_user = get_user(request)
        if request.method == "POST":
            TaskUsers.objects.filter(id=task_id).update(
                completed=True,
                completed_date=timezone.now() 
                )
            TaskHistory.objects.create(
            user=current_user,
            task=task,
            complete=True
        )
        return redirect('tasks:my_active_task')

def open_task(request, task_id):
        task = TaskUsers.objects.get(id=task_id)
        current_user = get_user(request)
            
        if request.method == "POST":
            TaskUsers.objects.filter(id=task_id).update(
                completed=False,
                completed_date=None,
                not_accepted=False
                )
            TaskHistory.objects.create(
            user=current_user,
            task=task,
            reopen=True
        )
        return redirect('tasks:my_completed_task')

def not_accept_task(request, task_id):
        completed_date=timezone.now()
        if request.method == "POST":
            TaskUsers.objects.filter(id=task_id).update(
                not_accepted=~F("not_accepted"),
                completed_date=completed_date,
                completed=False  
            )
        return redirect('tasks:my_active_task')

def delete_coment(request, coment_id):
    coment = Coment.objects.get(id=coment_id)
    task = coment.task
    current_user = get_user(request)
    task_id = TaskUsers.objects.filter(task=task, user=current_user).first().id
    if request.method == 'POST':
        content = f"user: {current_user}, delete comment from task: {task.title}, with content:{coment.content}."
        DeleteHistory.objects.create(user=current_user, content=content, comment=True)
        coment.delete()
    return redirect("tasks:detail_task", task_id=task_id)



####################################################################################################
#Old function. Do not use at the moment, there are class view

@login_required
def create_task(request):
    """Old function. Use CreateTaskView.as_view()"""
    template_name = 'tasks/create_task.html'
    current_user = get_user(request)
    date = timezone.localdate()
    current_employee = get_user_employee(user=current_user)
    recipients_query, recipients_type = employee_tasks_allowed_locations(current_user)
    positions = get_management_positions()
    # my_created_tasks = TaskUsers.objects.filter(user=current_user, creator=True)
    my_created_tasks = (Task.objects.
                            annotate(task_count=Count('taskusers')).
                            filter(taskusers__user=current_user).
                            annotate(creator=Q(taskusers__creator=True))
                            )
    form = TaskForm()
    task_for_my_location = Task.objects.annotate(task_count=Count('taskusers')).filter(
        Q(task_count__gt=1),
        )
    context = {
        "recipients": recipients_query,
        "recipients_type": recipients_type,
        "positions": positions,
        "tasks": my_created_tasks,

        "task_for_my_location": task_for_my_location,
        "form": form,
        "current_employee": current_employee,
        "date": date,
        "current_user": current_user,
    }
    if request.method == 'POST':
        form = TaskForm(request.POST)
        errors = form.errors
        context["errors"] = errors
        if form.is_valid():
            recipients_id_from_form = request.POST.getlist("recipients")
            users = users_to_tasks_create(recipients_list=recipients_id_from_form, recipients_type=recipients_query[0])
            form_data = form.cleaned_data
            title = form_data.get('title')
            content = form_data.get('content')
            location = get_user_location(current_user)
            deadline = form_data.get('deadline')
            start_date = form_data.get('start_date')
            
            task, created = Task.objects.get_or_create(
                title=title,
                content=content,
                location=location,
                deadline=deadline,
                start_date=start_date
            )
            task.recipients.set(users)
            task.recipients.add(current_user, through_defaults={"creator": True})
            return redirect('tasks:create_task')
    return render(request, template_name, context)

@login_required
def my_tasks(request):
    """Old function. Use MyTaskListView.as_view()"""
    template_name = 'tasks/list_tasks.html'
    current_user = get_user(request)
    date = timezone.localdate()
    task_users = TaskUsers.objects.filter(user=current_user)
    all_task=True
    context = {
        "date": date,
        "taskusers": task_users,
        "all_task": all_task
    }
    return render(request, template_name, context)

@login_required
def my_completed_task(request):
    """Old function. Use MyTaskListView.as_view()"""
    template_name = 'tasks/list_tasks.html'
    current_user = get_user(request)
    date = timezone.localdate()
    task_users = TaskUsers.objects.filter(user=current_user)
    completed_task = task_users.filter(Q(completed=True) | Q(not_accepted=True))
    completed = True
    context = {
        "date": date,
        "taskusers": completed_task,
        "completed": completed
    }
    return render(request, template_name, context)

@login_required
def my_active_task(request: HttpRequest ):
    """Old function. Use MyTaskListView.as_view()"""
    template_name = 'tasks/list_tasks.html'
    current_user = get_user(request)
    date = timezone.localdate()
    task_users = TaskUsers.objects.filter(user=current_user)
    active_task = task_users.exclude(Q(completed=True) | Q(not_accepted=True))
    active = True
    context = {
        "date": date,
        "taskusers": active_task,
        "active": active
    }
    return render(request, template_name, context)

@login_required
def my_location_tasks(request):
    """Old function. Use MyLocationTaskView.as_view()"""
    template_name = 'tasks/list_my_location_tasks.html'
    current_user = get_user(request)
    date = timezone.localdate()

    current_user_location = get_user_location(current_user)
    my_location_users = get_users_from_location(recipients_id=[current_user_location.id], recipients=current_user_location)
    location_task = Task.objects.filter(taskusers__user__in=my_location_users)

    list_task_new = Task.objects.filter(taskusers__user__in=my_location_users).annotate(
        count_completed =Count("taskusers", filter=Q(taskusers__completed=True)),
        total=Count("taskusers", filter=Q(taskusers__creator=False)),
        percent_completed = ExpressionWrapper(F('count_completed')*100/F('total'), output_field=DecimalField())
        )
    context = {
        "date": date,
        "list_task": list_task_new,
        "current_user": current_user,
    }
    return render(request, template_name, context)

def detail_location_task(request, task_id):
    """Old function. Use LocationTaskDetailView.as_view()"""
    template_name = "tasks/detail_location_task.html"
    current_user = get_user(request)
    date = timezone.localdate()
    current_user_location = get_user_location(current_user)
    my_location_users = get_users_from_location(recipients_id=[current_user_location.id], recipients=current_user_location)

    task = Task.objects.filter(id=task_id).first()
    task_users = TaskUsers.objects.filter(task=task)

    task_for_my_location = Task.objects.annotate(task_count=Count('taskusers')).filter(
        Q(task_count__gt=1),
        Q(id=task_id),
        ).first()
    
    context = {
        
        "task_users": task_users,
        "date": date,
        "object": task,
        "task_for_my_location": task_for_my_location,

        "my_location_users": my_location_users
    }   
    return render(request, template_name, context)
#######################################################################################################