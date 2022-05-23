import graphene
from graphql_jwt.decorators import login_required

from api.users.schema import UserObjectType


class UserQuery(graphene.ObjectType):
    user = graphene.Field(
        UserObjectType,
        description='Return Current User\'s Information'
    )

    @login_required
    def resolve_user(self, info):
        return info.context.user
