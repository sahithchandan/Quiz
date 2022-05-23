import graphene
import graphql_jwt


# As the app grows the Query and Mutation class will extend from more schemas
from api.quiz.mutation import QuizMutation
from api.quiz.query import QuizQuery
from api.users.mutation import UserMutation
from api.users.query import UserQuery


class Query(UserQuery, QuizQuery):
    pass


class Mutation(UserMutation, QuizMutation):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
