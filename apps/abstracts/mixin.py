from typing import Any

from django.core.cache import cache
from django.db.models import QuerySet
# DRF
from rest_framework.pagination import BasePagination
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK

class DRFResponsseMixin:
    """"Mixin to get DRF response"""
    def get_drf_response(
            self,
            request:DRFRequest,
            data:Any,
            serializer_class:type[Serializer],
            many:bool=False,
            paginator:BasePagination|None=None,
            status_code:int=HTTP_200_OK
    )->DRFResponse:
        """Serialize the data page by page"""
        serializer_context:dict[str,Any]={"request":request}
        if paginator and many:
            objects:list|None=paginator.paginate_queryset(
                queryset=data,request=request,view=self
            )
            serializer:Serializer=serializer_class(
                objects, many=many, context=serializer_context
            )
            return paginator.get_paginated_response(serializer.data)
        serializer=serializer_class(data,many=many,context=serializer_context)
        return DRFResponse(data=serializer.data,status=status_code)

class CachedListMixin:
    """Mixin to answer with a list that is kept in the cache"""
    def get_cached_list_response(
            self,
            request:DRFRequest,
            queryset:QuerySet,
            serializer_class:type[Serializer],
            cache_key:str,
            cache_timeout:int
    )->DRFResponse:
        """Take the list from cache or from database and save"""
        data:list[dict[str,Any]] | None=cache.get(cache_key)
        if data is None:
            serializer:Serializer=serializer_class(
            queryset, many=True, context={"request":request}
        )
            data=serializer.data
            cache.set(cache_key,data, timeout=cache_timeout)
        return DRFResponse(data=data,status=HTTP_200_OK)
        