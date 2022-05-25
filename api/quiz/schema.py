import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from api.quiz.models import Questionnaire, Questions, QuestionnaireResponses


class CountableConnectionBase(relay.Connection):
    """
        Extend connection class to display
        total count and edges count in paginated results
    """
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    @classmethod
    def resolve_total_count(cls, root, info, **kwargs):
        return root.length

    @classmethod
    def resolve_edge_count(cls, root, info, **kwargs):
        return len(root.edges)


class QuestionnaireNode(DjangoObjectType):
    """
        Questionnaire Object Node
    """

    class Meta:
        model = Questionnaire
        exclude = ['created_by', 'is_active']
        convert_choices_to_enum = False
        filter_fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)
        connection_class = CountableConnectionBase


class QuestionsNode(DjangoObjectType):
    """
        Questions Object Node
    """

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
        connection_class = CountableConnectionBase


class QuestionnaireResponsesNode(DjangoObjectType):
    """
        QuestionnaireResponses Object Node
    """
    sharable_link = graphene.String()

    class Meta:
        model = QuestionnaireResponses
        exclude = ['is_active']
        convert_choices_to_enum = False
        interfaces = (relay.Node,)
