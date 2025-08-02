# urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import post_search, CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.PostListView.as_view(template_name='blog/post_list.html'), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(template_name='blog/post_detail.html'), name='post-detail'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(template_name='blog/post_confirm_delete.html'), name='post-delete'),
    path('search/', post_search, name='post-search'),
    path('tags/<str:tag_name>/', post_search, name='tag-detail'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
]
