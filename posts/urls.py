from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.GroupPostListView.as_view(), name='group_post_list'),
    path('new/', views.CreatePostView.as_view(), name='create_post'),
    path('by/<username>/', views.UserPostListView.as_view(), name='user_post_list'),
    path('by/<username>/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
]