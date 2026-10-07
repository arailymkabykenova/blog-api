from django.contrib.admin import ModelAdmin, register

from apps.blog.models import Category, Comment, Post, Tag


@register(Post)
class PostAdmin(ModelAdmin):
    """register Post model in admin panel"""


@register(Comment)
class CommentAdmin(ModelAdmin):
    """register Comment model in admin panel"""


@register(Category)
class CategoryAdmin(ModelAdmin):
    """register Category model in admin panel"""


@register(Tag)
class TagAdmin(ModelAdmin):
    """register Tag model in admin panel"""
