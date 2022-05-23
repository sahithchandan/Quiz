"""
    User Schema
"""
from graphene_django.types import DjangoObjectType
from api.users.models import User


class UserObjectType(DjangoObjectType):
    """
        User Object Type
    """

    class Meta:
        """
            Meta class
        """
        model = User
        exclude_fields = ['password']
