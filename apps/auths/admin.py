from unfold.admin import ModelAdmin
from django.contrib.admin import register, site
from django.contrib.auth.models import Group
from apps.auths.models import User
site.unregister(Group)

@register(User)
class UserAdmin(ModelAdmin):
    """register User model in admin panel"""

@register(Group)
class GroupAdmin(ModelAdmin):
    """register Group model in admin panel"""