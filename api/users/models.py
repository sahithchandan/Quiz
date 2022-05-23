from django.contrib.auth.models import AbstractUser

from api.models import TimestampedAbstractModel


class User(AbstractUser, TimestampedAbstractModel):

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email}" if self.email else f"{self.id}"
