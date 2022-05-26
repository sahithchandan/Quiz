import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from api.quiz.models import Questionnaire, QuestionnaireResponses
from api.quiz.schema import QuestionnaireNode, QuestionsNode, QuestionnaireResponsesNode
from api.utils import filter_objects


class QuizQuery(graphene.ObjectType):
    # questionnaires
    all_questionnaires = DjangoFilterConnectionField(QuestionnaireNode, by_me=graphene.Boolean())
    questionnaire = relay.Node.Field(QuestionnaireNode)

    # questionnaire response
    all_questionnaire_responses = DjangoFilterConnectionField(QuestionnaireResponsesNode)
    questionnaire_responses = graphene.Field(QuestionnaireResponsesNode,
                                             id=graphene.ID(required=True))

    # questions
    all_questions = DjangoFilterConnectionField(QuestionsNode)

    @login_required
    def resolve_all_questionnaires(self, info, **kwargs):
        by_me = kwargs.get('by_me', False)
        if by_me:
            return Questionnaire.filter.by_user(info.context.user)
        return Questionnaire.objects.all()

    @login_required
    def resolve_all_questionnaire_responses(self, info, **kwargs):
        return QuestionnaireResponses.filter.by_user(
            info.context.user).with_select_related().with_prefetch_related()

    @login_required
    def resolve_questionnaire_responses(self, info, **kwargs):
        return filter_objects(
            QuestionnaireResponses, kwargs['id']
        ).by_user(
            info.context.user
        ).with_select_related().with_prefetch_related('questions').first()
