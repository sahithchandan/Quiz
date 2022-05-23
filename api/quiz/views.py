from rest_framework import generics

from api.quiz.models import Questionnaire
from api.quiz.serializers import QuestionnaireRetrieveSerializer


class QuestionnaireRetrieveView(generics.RetrieveAPIView):
    """
         Questionnaire retrieve view
    """
    serializer_class = QuestionnaireRetrieveSerializer
    queryset = Questionnaire.filter.with_prefetch_related().all()
