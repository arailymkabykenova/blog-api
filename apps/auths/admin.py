from django.contrib.admin import register, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from apps.auths.models import User
site.unregister(Group)

@register(User)
class UserAdmin(BaseUserAdmin,ModelAdmin):
    """register User model in admin panel"""
    search_fields=("first_name","last_name","email")
    form=UserChangeForm
    add_form=UserCreationForm
    change_password_form=AdminPasswordChangeForm

    ordering=("email",)
    list_display=("email","first_name","last_name","is_staff","is_active")
    fieldsets=(
        (
            "Personal Info",
         {
             "classes":("tab",),
             "fields":(
                 "email",
                 "first_name",
                 "last_name",
                 "password" 
             ),
         },
         ),
        (
            "Permissions",
            {
                "classes":("tab",),
                "fields":(
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
                )
            },
        ),
        (
            "Important dates",
            {   "classes":("tab",),
                "fields":(
                "last_login",
            )
             },
        )
     )
    add_fieldsets=(
        (
            "Personal info",
            {
            "fields":(
                "email",
                "first_name",
                "last_name",
                "password" 
        ),
            },
        ),
    )
    
    


@register(Group)
class GroupAdmin(ModelAdmin):
    """register Group model in admin panel"""