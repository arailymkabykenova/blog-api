from datetime import date,timedelta
from django.utils import timezone
from django.db.models import QuerySet
from apps.blog.models import Post,Category,StatusType
from apps.auths.models import User

NEWEST_POSTS_COUNT=5
PAGE_SIZE=10

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

def post_by_slug(slug:str)->Post|None:
    """Return post by slug"""
    return Post.objects.filter(slug=slug).first()

def published_posts_page(page:int)->QuerySet[Post]:
    """Return posts by page"""
    start_page=(page-1)*PAGE_SIZE
    return published_posts()[start_page:start_page+PAGE_SIZE]

def posts_with_word_in_title(word:str)->QuerySet[Post]:
    """Return posts with "word" in title"""
    return Post.objects.filter(title__icontains=word)

def users_with_email_domain(domain:str)->QuerySet[User]:
    """Return emails with certain domain"""
    return User.objects.filter(email__iendswith="@"+domain)

def posts_without_category()->QuerySet[Post]:
    """return posts without category"""
    return Post.objects.filter(category__isnull=True)

def categories_by_slug(slugs:list[str])->QuerySet[Category]:
    """Return categories whose slug is in the list"""
    return Category.objects.filter(slug__in=slugs)

def posts_in_month(year:int,month:int)->QuerySet[Post]:
    """Return posts created in this month of this year"""
    return Post.objects.filter(created_at__year=year,created_at__month=month)

def posts_last_days(days:int)->QuerySet[Post]:
    """Posts created in the last "days" days"""
    return Post.objects.filter(created_at__gte=timezone.now()-timedelta(days=days))

def posts_between(start:date,end:date)->QuerySet[Post]:
    """Return posts created from start to end"""
    return Post.objects.filter(created_at__date__range=(start,end))

def author_published_posts(email:str)->QuerySet[Post]:
    """Return published posts of the author with this email"""
    return Post.objects.filter(status=StatusType.PUBLISHED,author__email__iexact=email)



QUERIES={1:categories_by_name, 2:published_posts, 3:newest_published_posts, 4:post_by_slug, 5:active_users_count, 6:has_drafts, 7:published_posts_page,
         8:posts_with_word_in_title, 9:users_with_email_domain, 10:posts_without_category,11:categories_by_slug, 12:posts_in_month, 13:posts_last_days,
         14:posts_between, 15:author_published_posts}