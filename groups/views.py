from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember


class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group


class GroupDetailView(generic.DetailView):
    model = Group


class ListGroupView(generic.ListView):
    model = Group
