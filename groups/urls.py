from django.urls import path
from . import views


app_name = 'groups'

urlpatterns = [
    path('', views.ListGroupView.as_view(), name='all_groups'),
    path('new/', views.CreateGroupView.as_view(), name='create_group'),
    path('posts/in/<slug>', views.GroupDetailView.as_view(), name='group_detail'),
    path('join/<slug>/', views.JoinGroupView.as_view(), name='join_group'),
    path('leave/<slug>/', views.LeaveGroupView.as_view(), name='leave_group'),
]