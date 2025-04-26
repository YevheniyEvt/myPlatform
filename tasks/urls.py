from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('all/', views.MyTaskListView.as_view(), name='my_tasks'),
    path('active/', views.MyTaskListView.as_view(), name='my_active_task'),
    path('completed/', views.MyTaskListView.as_view(), name='my_completed_task'),

    path('<int:pk>/', views.TaskDetailCommentView.as_view(), name='detail_task'),
    path('<int:pk>/<int:user_id>/', views.TaskDetailCommentView.as_view(), name='detail_task'),

    path('location/', views.MyLocationTaskView.as_view(), name='my_location_tasks'),
    path('location/<int:pk>/', views.LocationTaskDetailView.as_view(), name='detail_location_task'),
    
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete_task'),

    path('delete/coment/<int:pk>', views.CommentDeleteView.as_view(), name='delete_coment'),

    path('complate/<int:task_id>', views.complete_task, name='complete_task'),
    path('open/<int:task_id>', views.open_task, name='open_task'),
    path('not-accept/<int:task_id>', views.not_accept_task, name='not_accept_task'),
    



    
]
