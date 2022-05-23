from rest_framework import generics
from rest_framework.response import Response

from api.quiz.choices import QuestionnaireProgressChoices
from api.quiz.models import QuestionnaireUserAnswers
from api.quiz.serializers import QuestionnaireUserAnswersRetrieveSerializer


class QuestionnaireUserAnswersRetrieveView(generics.RetrieveAPIView):
    """
         Questionnaire retrieve view
    """
    serializer_class = QuestionnaireUserAnswersRetrieveSerializer
    queryset = QuestionnaireUserAnswers.filter.not_started().with_select_related().all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.progress = QuestionnaireProgressChoices.IN_PROGRESS
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
