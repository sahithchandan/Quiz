from graphql_relay import to_global_id
from rest_framework import serializers

from api.quiz.models import Questionnaire, QuestionnaireUserAnswers
from api.quiz.schema import QuestionnaireNode, QuestionnaireUserAnswersNode


class QuestionnaireSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    @staticmethod
    def get_id(obj):
        return to_global_id(QuestionnaireNode.__name__, obj.id)

    class Meta:
        model = Questionnaire
        fields = ["id", "title"]


class QuestionnaireUserAnswersRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    questionnaire = QuestionnaireSerializer()

    @staticmethod
    def get_id(obj):
        return to_global_id(QuestionnaireUserAnswersNode.__name__, obj.id)

    @staticmethod
    def get_total_questions(obj):
        return obj.questionnaire.questions.count()

    class Meta:
        model = QuestionnaireUserAnswers
        fields = ["id", "created_at", "progress", "questionnaire", "total_questions"]
