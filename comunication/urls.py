from django.urls import path
from . import views

app_name = 'comunication'
urlpatterns = [
    path('articles/', views.news_list, name='list_article'),
    path('copmetitions/', views.competition_list, name='competition_list'),
    path('news/', views.global_news_list, name='global_news_list'),
    path('<int:pk>/', views.detail_article, name='detail_article'),

    path('article/create/', views.CreateArticle.as_view(), name='create_article'),
    path('article/update/<int:pk>/', views.UpdateArticle.as_view(), name='update_article'),
    path('article/delete/<int:pk>/', views.DeleteArticle.as_view(), name='delete_article'),
    path('delete/coment/<int:pk>/', views.delete_coment, name='delete_coment'),
]