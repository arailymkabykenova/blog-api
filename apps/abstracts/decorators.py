from collections.abc import Callable
from functools import wraps
from typing import Any,TypeVar

from django.db.models import Manager,Model,QuerySet

from rest_framework.serializers import Serializer
from rest_framework.response import Response as DRFResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND

T=TypeVar("T",bound=Model)
QuerysetSource=QuerySet[T]| Manager[T]| Callable[[Any,DRFRequest],QuerySet[T]]
def validate_serializer_data(
        serializer_class:type[Serializer],
        many:bool=False,
)->Callable:
    """Decorator to validate the request data with the given serializer"""

    def decorator(func:Callable[...,DRFResponse])->Callable[..., DRFResponse]:
        @wraps(func)
        def wrapper(
            self:Any,
            request:DRFRequest,
            *args:Any,
            **kwargs:Any,
        )->DRFResponse:
            """Run the view only if the data is valid,otherwise answer 400"""
            local_context:dict[str,Any]={"request":request}
            if request.method in ("POST","PUT","PATCH"):
                data=request.data
            else:
                data=request.query_params
            if "object" in kwargs:
                local_context["object"]=kwargs["object"]

            serializer:Serializer=serializer_class(
                instance=local_context.get("object"),
                data=data,
                context=local_context,
                many=many,
                partial=request.method=="PATCH",
            )
            if not serializer.is_valid():
                return DRFResponse(
                    data=serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
            kwargs["validated_data"]=serializer.validated_data.copy()
            kwargs["serializer"]=serializer
            return func(self,request,*args,**kwargs)
        return wrapper
    return decorator

def find_queryset_object_by_query_pk(
        queryset:QuerysetSource,
        entity_name:str
)->Callable:
    """Decorator to find an object by the pk from the URL"""
    def decorator(func:Callable[...,DRFResponse])->Callable[...,DRFResponse]:
        @wraps(func)
        def wrapper(
            self:Any,
            request:DRFRequest,
            *args:Any,
            **kwargs:Any,
        )->DRFResponse:
            """Put the found object into kwargs["object"] or answer 400/404"""
            pk:str|None=kwargs.get("pk")
            if not pk or not pk.isdigit():
                return DRFResponse(
                    data={"details":[f"{entity_name} ID must be a number."]},
                    status=HTTP_400_BAD_REQUEST,
                )
            found_queryset:QuerySet[T]| Manager[T]=(
                queryset(self,request) if callable(queryset) else queryset
            )
            try:
                kwargs["object"]=found_queryset.get(pk=pk)
            except found_queryset.model.DoesNotExist:
                return DRFResponse(
                    data={"details":[f"{entity_name} with ID {pk} hasn't been found."]},
                    status=HTTP_404_NOT_FOUND
                )    
            return func(self,request,*args,**kwargs)
        return wrapper
    return decorator
