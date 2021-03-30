from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib.auth import get_user_model
from braces.views import SelectRelatedMixin
from . import models

User = get_user_model()


class GroupPostListView(SelectRelatedMixin, generic.ListView):  # posts of the group
    model = models.Post
    select_related = ('user', 'group')


class UserPostListView(generic.ListView):  # posts of the user
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user  # used in user_post_list.html
        return context


class PostDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePostView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('text', 'group')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  # connecting the user with the post
        self.object.save()
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:group_post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post deleted.')
        return super().delete(*args, **kwargs)
