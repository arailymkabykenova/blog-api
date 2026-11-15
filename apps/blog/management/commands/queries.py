from typing import Any
from django.core.management.base import BaseCommand,CommandError,CommandParser
from django.db.models import QuerySet
from django.test.utils import CaptureQueriesContext
from django.db import connection
from apps.blog.queries import QUERIES
from apps.blog.models import Post

MAX_LENGTH_OF_PRINT=5
PAGE_START=2

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
            7:{"page":PAGE_START}
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
