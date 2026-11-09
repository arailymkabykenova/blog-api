from django.contrib.admin import register
from django.db.models import Count
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import display

from apps.blog.models import Category, Comment, Post, StatusType, Tag


@register(Post)
class PostAdmin(ModelAdmin):
    """register Post model in admin panel"""
    list_display=("title","author","status_label","comments_count","category","created_at")
    search_fields=("title","body","author__email")
    list_filter=("status","category",("created_at",RangeDateTimeFilter))
    prepopulated_fields={"slug":("title",)} # noqa: RUF012
    autocomplete_fields=("author","category","tags")
    list_select_related=("author","category")
    list_filter_submit=True
    #list select related ->1 join ->достает нам пост сразу с автором и категорией
    readonly_fields=("created_at","updated_at")
    warn_unsaved_form=True
    @display(
        description="Status",
        label={
            StatusType.PUBLISHED:"success",
            StatusType.DRAFT:"warning"
        }
    )
    def status_label(self,obj:Post)->tuple[str,str]:
                return obj.status,obj.get_status_display()
    
    @display(
                description="Comments",
                ordering="comments_count"
    )
    def comments_count(self,obj:Post)->int:
            return obj.comments_count

    def get_queryset(self, request):
                  return super().get_queryset(request).annotate(comments_count=Count("comments"))
    
    
@register(Comment)
class CommentAdmin(ModelAdmin):
    """register Comment model in admin panel"""
    BODY_PREVIEW_LENGTH=50
    list_display=("post","author","body_preview","created_at")
    search_fields=("body","author__email","post__title")
    autocomplete_fields=("author","post")
    list_select_related=("post","author")
    list_filter=(("created_at",RangeDateTimeFilter))
    list_filter_submit=True
    @display(
                description="Body",
    ) 
    def body_preview(self,obj:Comment)->str:
          if len(obj.body)>self.BODY_PREVIEW_LENGTH:
                return obj.body[:self.BODY_PREVIEW_LENGTH]+"..."
          else:
                return obj.body
          
    


@register(Category)
class CategoryAdmin(ModelAdmin):
    """register Category model in admin panel"""
    list_display=("name","slug","posts_count")
    search_fields=("name",)
    prepopulated_fields={"slug":("name",)} # noqa: RUF012
    @display(
            description="Posts",
            ordering="posts_count"
            )
    def posts_count(self,obj:Category)->int:
            return obj.posts_count

    def get_queryset(self, request):
            return super().get_queryset(request).annotate(posts_count=Count("post"))
    



@register(Tag)
class TagAdmin(ModelAdmin):
    """register Tag model in admin panel"""
    list_display=("name","slug","posts_count")
    search_fields=("name",)
    prepopulated_fields={"slug":("name",)} # noqa: RUF012
    @display(
            description="Posts",
            ordering="posts_count"
        )
    def posts_count(self,obj:Tag)->int:
            return obj.posts_count

    def get_queryset(self, request):
            return super().get_queryset(request).annotate(posts_count=Count("posts"))
    

