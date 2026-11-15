from django.db.models import QuerySet
from apps.blog.models import Post,Category,StatusType
from apps.auths.models import User

NEWEST_POSTS_COUNT=5
def categories_by_name()->QuerySet[Category]:
    """Return categories by name"""
    return Category.objects.order_by("name")

def published_posts()->QuerySet[Post]:
    """Return published posts, newest first"""
    return Post.objects.filter(status=StatusType.PUBLISHED).order_by("-created_at")

def newest_published_posts()->QuerySet[Post]:
    """Return 5 newest published posts"""
    return published_posts()[:NEWEST_POSTS_COUNT]

def active_users_count()->int:
    """Return number of active users"""
    return User.objects.filter(is_active=True,is_staff=False).count()

def has_drafts()->bool:
    """Return true if at least one draft exists"""
    return Post.objects.filter(status=StatusType.DRAFT).exists()

QUERIES={1:categories_by_name, 2:published_posts, 3:newest_published_posts, 5:active_users_count, 6:has_drafts}