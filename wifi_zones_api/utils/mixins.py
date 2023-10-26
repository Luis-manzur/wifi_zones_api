"""Custom model mixins"""
# Django
from django.core.cache import cache
# DRF
from rest_framework import mixins
from rest_framework.response import Response


class CacheListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        data = cache.get(request.path)
        if not data or request.query_params:
            response = super().list(request, *args, **kwargs)
            data = response.data
            if not request.query_params:
                cache.set(request.path, data, self.get_cache_timeout())

        return Response(data)


class CacheListPrivateModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        data = cache.get(request.path + str(request.user.pk))
        if not data or request.query_params:
            response = super().list(request, *args, **kwargs)
            data = response.data
            if not request.query_params:
                cache.set(request.path + str(request.user.pk), data, self.get_cache_timeout())

        return Response(data)


class CacheRetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        data = cache.get(request.path)
        if not data:
            response = super().retrieve(request, *args, **kwargs)
            data = response.data
            cache.set(request.path, data, self.get_cache_timeout())

        return Response(data)
