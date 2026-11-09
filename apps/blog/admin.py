
from django.contrib.admin import register
from unfold.admin import ModelAdmin
from unfold.decorators import display
from apps.blog.models import Category, Comment, Post, Tag, StatusType


@register(Post)
class PostAdmin(ModelAdmin):
    """register Post model in admin panel"""
    list_display=("title","author","status_label","category","created_at")
    search_fields=("title","body","author__email")
    list_filter=("status","category")
    prepopulated_fields={"slug":("title",)}
    autocomplete_fields=("author","category","tags")
    list_select_related=("author","category")
    #list select related ->1 join ->достает нам пост сразу с автором и категорией
    readonly_fields=("created_at","updated_at")
    @display(
        description="Status",
        label={
            StatusType.PUBLISHED:"success",
            StatusType.DRAFT:"warning"
        }
    )
    def status_label(self,obj:Post)->tuple[str,str]:
                return obj.status,obj.get_status_display()
    

@register(Comment)
class CommentAdmin(ModelAdmin):
    """register Comment model in admin panel"""
    list_display=("post","author","body","created_at")
    search_fields=("body","author__email","post__title")
    autocomplete_fields=("author","post")
    list_select_related=("post","author")


@register(Category)
class CategoryAdmin(ModelAdmin):
    """register Category model in admin panel"""
    list_display=("name","slug")
    search_fields=("name",)
    prepopulated_fields={"slug":("name",)}



@register(Tag)
class TagAdmin(ModelAdmin):
    """register Tag model in admin panel"""
    list_display=("name","slug")
    search_fields=("name",)
    prepopulated_fields={"slug":("name",)}

