from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/create/', views.post_new, name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('author/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.PostListbyAuthorView.as_view(),
         name='author_detail'),
    path('post/<int:pk>/comment/', views.CommentCreate.as_view(), name='comment'),
]
