
from faker import Faker
from random import Random
from random import choice
from time import perf_counter
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth.hashers import make_password
from apps.auths.models import User
from apps.blog.models import Category, Tag, Post, Comment, StatusType 



class Command(BaseCommand):
    MAIL_BOX_DOMAINS=(
        "kbtu.kz",
        "23bd.kz"
    )
    SEED_PASSWORD = "12345"
    CATEGORY_NAMES = (
        "Python",
        "Django",
        "DevOps",
        "Databases",
        "Frontend",
        "Machine Learning",
        "Security",
        "Career"
    )
    TAG_NAMES = (
        "Docker","Kubernetes","PostgreSQL","Redis","Git","Linux","Testing","REST API","Async","Celery","ORM","Performance","CI/CD","AWS","Pandas","React","TypeScript","Authentication","Debugging","Best Practices"
    )
    DEFAULT_USER = 20
    DEFAULT_POST = 100
    DEFAULT_COMMENT = 500
    STAFF_PROPORTION = 0.2
    IS_ACTIVE_PROPORTION = 0.8
    help="Generate seed data for the application"
    PROPORTION_OF_PUBLISHED=0.7
    PROPORTION_OF_DRAFT=0.3
    PROPORTION_WITHOUT_CATEGORY=0.1
    MAX_TAGS_PER_POST=5
    faker=Faker()
    randomizer=Random()
    PARAGRAPH_LENGTH=3
    COMMENT_SENTENCES_LENGTH_MAX=3
    COMMENT_SENTENCES_LENGTH_MIN=1
    
    def create_email(self,first_name:str,last_name:str)->str:
        return f"{first_name.lower()}.{last_name.lower()}@"+ choice(self.MAIL_BOX_DOMAINS)

    def create_first_last_name_with_email(self)->tuple[str,str,str]:
        first_name=self.faker.first_name()
        last_name=self.faker.last_name()
        email=self.create_email(first_name,last_name)
        return first_name,last_name,email

    def generate_users(self,number:int)->int:
        users_to_create:list[User]=[]
        user_email=set(User.objects.values_list("email",flat=True))
        hashed_password=make_password(self.SEED_PASSWORD)
        for _ in range(number):
            random_indicator_staff_active=self.randomizer.random()
            first_name,last_name,email=self.create_first_last_name_with_email()
            if random_indicator_staff_active<self.STAFF_PROPORTION:
                is_staff=True
            else:
                is_staff=False
            if random_indicator_staff_active<=self.IS_ACTIVE_PROPORTION:
                is_active=True
            else:
                is_active=False
            while email in user_email:
                first_name,last_name,email=self.create_first_last_name_with_email()
            user_email.add(email)
            users_to_create.append(User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,
                is_staff=is_staff,
                is_active=is_active
            )
            )
        return len(User.objects.bulk_create(users_to_create))


    def generate_categories(self)->int:
        categories_to_create:list[Category]=[]
        category_name=set(Category.objects.values_list("name",flat=True))
        for name in self.CATEGORY_NAMES:
            if name not in category_name:
                categories_to_create.append(Category(name=name,slug=slugify(name)))
        return len(Category.objects.bulk_create(categories_to_create))

    def generate_tags(self)->int:
        tags_to_create:list[Tag]=[]
        tag_names=set(Tag.objects.values_list("name",flat=True))
        for name in self.TAG_NAMES:
            if name not in tag_names:
                tags_to_create.append(Tag(name=name,slug=slugify(name)))
        return len(Tag.objects.bulk_create(tags_to_create))

    def generate_posts(self,number:int)->int:
        posts_to_create:list[Post]=[]
        users=list(User.objects.all())
        if len(users)==0:
            raise CommandError("No users found. Please generate users first.")
        categories=list(Category.objects.all())
        tags=list(Tag.objects.all())
        used_slugs=set(Post.objects.values_list("slug",flat=True))
        for _ in range(number):
            author=self.randomizer.choice(users)
            title=self.faker.sentence()
            slug=slugify(title)
            if slug in used_slugs:
                base_slug=slug
                counter=2
                while slug in used_slugs:
                    slug=f"{base_slug}-{counter}"
                    counter+=1
            used_slugs.add(slug)
            body="\n\n".join(self.faker.paragraphs(nb=self.PARAGRAPH_LENGTH))
            random_status=self.randomizer.random()
            if random_status<=self.PROPORTION_OF_PUBLISHED:
                status=StatusType.PUBLISHED
            else:
                status=StatusType.DRAFT
            if (len(categories)==0) or (self.randomizer.random()<=self.PROPORTION_WITHOUT_CATEGORY):
                category=None
            else:
                category=self.randomizer.choice(categories)

            post=Post(
                author=author,
                title=title,
                slug=slug,
                body=body,
                status=status,
                category=category
            )
            
            posts_to_create.append(post)
        created_posts=Post.objects.bulk_create(posts_to_create)
        for post in created_posts:
            num_tags=self.randomizer.randint(0,min(self.MAX_TAGS_PER_POST,len(tags)))
            post_tags=self.randomizer.sample(tags,num_tags)
            post.tags.set(post_tags)
        return len(created_posts)

    def generate_comments(self,number:int)->int:
        users=list(User.objects.all())
        if len(users)==0:
            raise CommandError("No users found. Run seed command")
        posts=list(Post.objects.filter(status=StatusType.PUBLISHED))
        if len(posts)==0:
            raise CommandError("No posts found. Run seed command")
        comments_to_create:list[Comment]=[]
        for _ in range(number):
            post=self.randomizer.choice(posts)
            author=self.randomizer.choice(users)
            body=" ".join(self.faker.sentences(nb=self.randomizer.randint(self.COMMENT_SENTENCES_LENGTH_MIN,self.COMMENT_SENTENCES_LENGTH_MAX)))
            comment=Comment(
                author=author,
                post=post,
                body=body
            )
            comments_to_create.append(comment)
        return len(Comment.objects.bulk_create(comments_to_create))

    def add_arguments(self, parser:CommandParser)->None:
        parser.add_argument(
            "--users",
            type=int,
            default=self.DEFAULT_USER,
            help="Number of users to create"
        )
        parser.add_argument(
            "--posts",
            type=int,
            default=self.DEFAULT_POST,
            help="Number of posts to create"
        )
        parser.add_argument(
            "--comments",
            type=int,
            default=self.DEFAULT_COMMENT,
            help="Number of comments ro create"
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all data before seedng"
        )

        
    def handle(self,*args,**options)->None:
        start_time=perf_counter()
        users_count=options["users"]
        posts_count=options["posts"]
        comments_count=options["comments"]
        if users_count<0 or posts_count<0 or comments_count<0:
            raise CommandError("Number of users,posts,comments must be non negative")
        if options["clear"]:
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Tag.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("All data cleared")

        generated_users=self.generate_users(users_count)
        generated_tags=self.generate_tags()
        generated_categories=self.generate_categories()
        generated_posts=self.generate_posts(posts_count)
        generated_comments=self.generate_comments(comments_count)

        self.stdout.write(f"Users {generated_users} created.")
        self.stdout.write(f"Tags {generated_tags} created.")
        self.stdout.write(f"Categories {generated_categories} created.")
        self.stdout.write(f"Posts {generated_posts} created.")
        self.stdout.write(f"Comments {generated_comments} created.")
        self.stdout.write(
            self.style.SUCCESS(f"Done in {perf_counter()-start_time:.2f} seconds")
        )

       