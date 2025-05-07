from django.urls import path
from . import views

app_name = 'comunication'
urlpatterns = [
    path('articles/', views.NewsListView.as_view(), name='list_article'),
    path('copmetitions/', views.CompetitionListView.as_view(), name='competition_list'),
    path('news/', views.GlobalNewsListView.as_view(), name='global_news_list'),
    path('<int:pk>/', views.ArticleCommentView.as_view(), name='detail_article'),

    path('article/create/', views.CreateArticle.as_view(), name='create_article'),
    path('article/update/<int:pk>/', views.UpdateArticle.as_view(), name='update_article'),
    path('article/delete/<int:pk>/', views.DeleteArticle.as_view(), name='delete_article'),
    path('delete/coment/<int:pk>/', views.DeleteComment.as_view(), name='delete_coment'),
]