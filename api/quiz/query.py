import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from api.quiz.models import Questionnaire, QuestionnaireResponses
from api.quiz.schema import QuestionnaireNode, QuestionsNode, QuestionnaireResponsesNode
from api.utils import filter_objects


class QuizQuery(graphene.ObjectType):
    # questionnaires
    all_questionnaires = DjangoFilterConnectionField(QuestionnaireNode, by_me=graphene.Boolean())
    questionnaire = relay.Node.Field(QuestionnaireNode)

    # questionnaire response
    all_questionnaire_responses = DjangoFilterConnectionField(QuestionnaireResponsesNode,
                                                              questionnaire_id=graphene.String(required=False))
    questionnaire_responses = graphene.Field(QuestionnaireResponsesNode,
                                             id=graphene.ID(required=True))

    # questions
    all_questions = DjangoFilterConnectionField(QuestionsNode)

    @login_required
    def resolve_all_questionnaires(self, info, **kwargs):
        by_me = kwargs.get('by_me', False)
        if by_me:
            return Questionnaire.filter.created_by(info.context.user)
        return Questionnaire.objects.all()

    @login_required
    def resolve_all_questionnaire_responses(self, info, **kwargs):
        queryset = QuestionnaireResponses.filter.created_by(
            info.context.user).with_select_related().with_prefetch_related()

        questionnaire_id = kwargs.get('questionnaire_id')
        if questionnaire_id:
            queryset = queryset.for_questionnaires(from_global_id(questionnaire_id)[1])

        return queryset

    @login_required
    def resolve_questionnaire_responses(self, info, **kwargs):
        return filter_objects(
            QuestionnaireResponses, kwargs['id']
        ).created_by(
            info.context.user
        ).with_select_related().with_prefetch_related('questions').first()
