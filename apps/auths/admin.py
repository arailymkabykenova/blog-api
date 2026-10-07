from django.contrib.admin import ModelAdmin, register

from apps.auths.models import User


@register(User)
class UserAdmin(ModelAdmin):
    """register User model in admin panel"""