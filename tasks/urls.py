from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('all/', views.MyTaskListView.as_view(), name='my_tasks'),
    path('active/', views.MyTaskListView.as_view(), name='my_active_task'),
    path('completed/', views.MyTaskListView.as_view(), name='my_completed_task'),

    path('<int:task_id>/', views.detail_task, name='detail_task'),
    
    path('location/', views.MyLocationTaskView.as_view(), name='my_location_tasks'),
    path('location/<int:pk>/', views.LocationTaskDetailView.as_view(), name='detail_location_task'),

    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complate/<int:task_id>', views.complete_task, name='complete_task'),
    path('open/<int:task_id>', views.open_task, name='open_task'),
    path('not-accept/<int:task_id>', views.not_accept_task, name='not_accept_task'),
    
    path('delete/coment/<int:coment_id>', views.delete_coment, name='delete_coment'),


    
]
