from django.contrib import admin
from . import models


class GroupMemberInline(admin.TabularInline):  # to edit members is a group
    model = models.GroupMember


admin.site.register(models.Group)
