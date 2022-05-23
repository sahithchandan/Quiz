from graphql_relay import to_global_id
from rest_framework import serializers

from api.quiz.models import Questionnaire
from api.quiz.schema import QuestionnaireNode


class QuestionnaireRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()

    @staticmethod
    def get_id(obj):
        return to_global_id(QuestionnaireNode._meta.name, obj.id)

    @staticmethod
    def get_total_questions(obj):
        return obj.questions.count()

    class Meta:
        model = Questionnaire
        fields = ["id", "title", "total_questions"]
