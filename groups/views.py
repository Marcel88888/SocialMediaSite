from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group


class GroupDetailView(generic.DetailView):
    model = Group


class ListGroupView(generic.ListView):
    model = Group


class JoinGroupView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:group_detail', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, f"You are already a member of {group.name} group.")
        else:
            messages.success(self.request, f"You are now a member of the {group.name} group.")

        return super().get(request, *args, **kwargs)


class LeaveGroupView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:group_detail', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, f"You are not a member of {group.name} group.")
        else:
            membership.delete()
            messages.success(self.request, f"You have left the {group.name} group.")

        return super().get(request, *args, **kwargs)

