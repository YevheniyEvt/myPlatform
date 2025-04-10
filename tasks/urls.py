from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.my_tasks, name='my_tasks'),
    path('active/', views.my_active_task, name='my_active_task'),
    path('completed/', views.my_completed_task, name='my_completed_task'),
    path('<int:task_id>/', views.detail_task, name='detail_task'),
    
    path('location/', views.my_location_tasks, name='my_location_tasks'),
    path('location/<int:task_id>/', views.detail_location_task, name='detail_location_task'),

    path('create/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complate/<int:task_id>', views.complete_task, name='complete_task'),
    path('open/<int:task_id>', views.open_task, name='open_task'),
    path('not-accept/<int:task_id>', views.not_accept_task, name='not_accept_task'),
    
    path('delete/coment/<int:coment_id>', views.delete_coment, name='delete_coment'),


    
]
