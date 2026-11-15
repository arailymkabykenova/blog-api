from typing import Any
from datetime import timedelta
from django.core.management.base import BaseCommand,CommandError,CommandParser
from django.db.models import QuerySet
from django.utils import timezone
from django.test.utils import CaptureQueriesContext
from django.db import connection
from apps.blog.queries import QUERIES
from apps.blog.models import Post, StatusType
from apps.auths.models import User

MAX_LENGTH_OF_PRINT=5
PAGE_START=2
TITLE_CONTAIN_WORD="word"
DOMAIN="kbtu.kz"
MONTH=timezone.now().month
YEAR=timezone.now().year
DAY_IN_MONTH=30 
END_DATE=timezone.now().date()
SAMPLE_CATEGORY_SLUGS = ["python", "django"]

class Command(BaseCommand):
    help="Run needed function by number"

    def add_arguments(self, parser:CommandParser)->None:
        parser.add_argument(
            "--number",
            type=int
        )
        parser.add_argument(
            "--sql",
            action="store_true"

        )

    def get_query_arguments(self)->dict[int,dict[str,Any]]:
        return{
            4:{"slug":Post.objects.values_list("slug",flat=True).first()},
            7:{"page":PAGE_START},
            8:{"word":TITLE_CONTAIN_WORD},
            9:{"domain":DOMAIN},
            11:{"slugs":SAMPLE_CATEGORY_SLUGS},
            12:{"year":YEAR,"month":MONTH},
            13:{"days":DAY_IN_MONTH},
            14:{"start":END_DATE-timedelta(days=DAY_IN_MONTH),"end":END_DATE},
            15:{"email":User.objects.filter(posts__status=StatusType.PUBLISHED).values_list("email", flat=True).first()}
        }

    

    def handle(self,*args,**options)->None:
        number=options["number"]
        if number is not None:
            if number not in QUERIES:
                raise CommandError("Doesn't exist")
            else:
                numbers=[number]
        else:
            numbers=list(QUERIES)

        arguments_by_number=self.get_query_arguments()
        for current in numbers:
            function=QUERIES[current]
            arguments=arguments_by_number.get(current,{})
            with CaptureQueriesContext(connection) as context:
                result=function(**arguments)
                if isinstance(result,QuerySet):
                    result=list(result)

            self.stdout.write(f"#{current} {function.__name__} - {len(context.captured_queries)} SQL query")
            if options["sql"]:
                for query in context.captured_queries:
                    self.stdout.write(f"{query["sql"]}")
            if isinstance(result,list):
                for row in result[:MAX_LENGTH_OF_PRINT]:
                    self.stdout.write(f" {row}")
                self.stdout.write(f" ({len(result)} rows)")
            else:
                self.stdout.write(f" {result}")
