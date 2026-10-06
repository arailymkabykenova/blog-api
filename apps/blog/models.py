from django.conf import settings
from django.db.models import (
    CharField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
    SlugField,
    Model,
    TextField,
    ManyToManyField,
    CASCADE,
    TextChoices
)

class Category(Model):
    NAME_MAX_LENGTH=100
    name=CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug=SlugField(unique=True)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self)->str:
        return self.name

class Tag(Model):
    NAME_MAX_LENGTH = 50
    name=CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug=SlugField(unique=True)

    def __str__(self)->str:
        return self.name

class Comment(Model):
    post=ForeignKey(
        to='Post',
        on_delete=CASCADE,
        related_name='comments'
    )
    author=ForeignKey(
            to=settings.AUTH_USER_MODEL,
            on_delete=CASCADE,
            related_name='comments'
    )
    body=TextField()
    created_at=DateTimeField(auto_now_add=True)

    def __str__(self)->str:
        return f'Comment by {self.author} on {self.post}'

class StatusType(TextChoices):
    DRAFT='draft', 'Draft'
    PUBLISHED='published', 'Published'


class Post(Model):
    TITLE_MAX_LENGTH = 200
    STATUS_MAX_LENGTH=10
    author=ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='posts'
    )
    title=CharField(max_length=TITLE_MAX_LENGTH)
    slug=SlugField(unique=True)
    body=TextField()
    category=ForeignKey(
        to=Category,
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    status=CharField(max_length=STATUS_MAX_LENGTH, choices=StatusType.choices, default=StatusType.DRAFT)
    tags=ManyToManyField(to=Tag, related_name='posts',blank=True)
    created_at=DateTimeField(auto_now_add=True)
    updated_at=DateTimeField(auto_now=True)

    def __str__(self)->str:
        return self.title
    
