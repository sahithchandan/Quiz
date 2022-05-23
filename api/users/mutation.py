import graphene
from graphql import GraphQLError

from api.users.models import User
from api.users.query import UserObjectType


class SignUp(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserObjectType)

    def mutate(self, info, email, password):
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
            return SignUp(user)
        except Exception as ex:
            raise GraphQLError(f'Something went wrong while creating user: Error: {ex}')


class UserMutation(graphene.ObjectType):
    signup = SignUp.Field()
