from django.urls import path


from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='topic_list'),
    path('<int:pk>/', views.TopicDetailCreateSectionView.as_view(template_name = 'notebook/topic_detail.html') ,name='topic_detail'),
    path('create-topic/', views.TopicCreateView.as_view(template_name = 'notebook/topic_list.html'), name='create_topic'),
    path('delete-topic/<int:pk>/', views.TopicDeleteView.as_view(), name='delete_topic'),

    path('delete-section/<int:pk>/', views.SectionDeleteView.as_view(), name='delete_section'),

    path('detail-section/<int:pk>/code/', views.CodeSectionView.as_view(template_name = 'notebook/section_detail.html') ,name='show_cod'),
    path('delete-code/<int:pk>/', views.CodeSectionDeleteView.as_view(), name='code_delete'),

    path('detail-section/<int:pk>/article/', views.ArticleSectionView.as_view(template_name = 'notebook/section_detail.html') ,name='show_articles'),
    path('delete-article/<int:pk>/', views.ArticleSectionDeleteView.as_view(), name='article_delete'),

    path('detail-section/<int:pk>/links/', views.LinksSectionView.as_view(template_name = 'notebook/section_detail.html') ,name='show_links'),
    path('delete-link/<int:pk>/', views.LinksSectionDeleteView.as_view(), name='link_delete'),

    path('detail-section/<int:pk>/images/', views.ImageSectionView.as_view(template_name = 'notebook/section_detail.html') ,name='show_images'),
    path('delete-image/<int:pk>/', views.ImageSectionDeleteView.as_view(), name='image_delete'),

    path('notes-list/', views.NoteView.as_view(), name='notes_list_view'),
    path('notes-list/update/<int:pk>/', views.NoteUpdateView.as_view(), name='notes_update_view'),
    path('notes-list/delete/<int:pk>/', views.NotesDelete.as_view(), name='notes_delete_view'),
]
