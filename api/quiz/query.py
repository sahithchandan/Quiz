import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from api.quiz.models import Questionnaire, Questions
from api.quiz.schema import QuestionnaireNode, QuestionsNode


class QuizQuery(graphene.ObjectType):
    # questionnaires
    all_questionnaires = DjangoFilterConnectionField(QuestionnaireNode)
    questionnaire = relay.Node.Field(QuestionnaireNode)

    # questions
    all_questions = DjangoFilterConnectionField(QuestionsNode)

    @staticmethod
    @login_required
    def resolve_all_questionnaires(root, info, **kwargs):
        return Questionnaire.objects.all()

    @staticmethod
    @login_required
    def resolve_all_questions(root, info, **kwargs):
        return Questions.objects.all()
