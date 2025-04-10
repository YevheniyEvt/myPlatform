from django.urls import path
from . import views

app_name = 'comunication'
urlpatterns = [
    path('articles', views.news_list, name='list_article'),
    path('copmetitions/', views.competition_list, name='competition_list'),
    path('news/', views.global_news_list, name='global_news_list'),
    path('<int:article_id>', views.detail_article, name='detail_article'),

    path('article/create/', views.create_article, name='create_article'),
    path('article/update/<int:article_id>', views.update_article, name='update_article'),
    path('article/delete/<int:article_id>', views.delete_article, name='delete_article'),
    path('delete/coment/<int:coment_id>', views.delete_coment, name='delete_coment'),
]