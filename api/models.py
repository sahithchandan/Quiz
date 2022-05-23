"""
    Abstract Models
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from api.managers import BaseModelManager


class TimestampedAbstractModel(models.Model):
    """
        Abstract model representing created and updated fields
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseModelManager(active=True)
    all_objects = BaseModelManager()
    inactive_objects = BaseModelManager(active=False)

    class Meta:
        abstract = True
