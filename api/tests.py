from graphene_django.utils import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from rest_framework.test import APITestCase, APIClient

from api.users.factories import UserFactory


class BaseGraphQLTestCase(GraphQLTestCase):

    def setUp(self, user=None):
        self.user = UserFactory() if user is None else user
        self.token = get_token(self.user)


class BaseAPITestCase(APITestCase):

    def setUp(self, user=None):
        self.user = UserFactory() if user is None else user
        self.user_client = APIClient()
