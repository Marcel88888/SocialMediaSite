from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import template
import misaka


User = get_user_model()
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # to get rid of whitespaces etc.
        self.description_html = misaka.html(self.description)  # to get markdown
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:group_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']  # the default ordering for the object, for use when obtaining lists of objects


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')

