from django.db import models


class BaseModelManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.is_active = kwargs.pop('active', None)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.is_active is None:
            return queryset
        return queryset.filter(is_active=self.is_active)


class BaseQueryManager(models.QuerySet):

    def with_ids(self, ids):
        if not isinstance(ids, list):
            ids = [ids]
        return self.filter(id__in=ids)
