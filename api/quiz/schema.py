import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from api.quiz.models import Questionnaire, Questions


class QuestionnaireNode(DjangoObjectType):
    sharable_link = graphene.String()

    class Meta:
        model = Questionnaire
        exclude = ['created_by', 'is_active']
        convert_choices_to_enum = False
        filter_fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class QuestionsNode(DjangoObjectType):

    class Meta:
        model = Questions
        exclude = ['is_active']
        convert_choices_to_enum = False
        filter_fields = filter_fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains', 'istartswith'],
            'type': ['exact'],
            'questionnaire__title': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)
