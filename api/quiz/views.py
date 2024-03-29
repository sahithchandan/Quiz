from rest_framework import generics
from rest_framework.response import Response

from api.quiz.choices import QuestionnaireProgressChoices
from api.quiz.models import QuestionnaireResponses
from api.quiz.serializers import QuestionnaireResponsesRetrieveSerializer


class QuestionnaireResponsesRetrieveView(generics.RetrieveAPIView):
    """
         Questionnaire Response retrieve view
    """
    serializer_class = QuestionnaireResponsesRetrieveSerializer
    queryset = QuestionnaireResponses.filter.with_select_related().all()
    lookup_url_kwarg = 'pin'

    def get_object(self):
        return self.queryset.with_pin(self.kwargs['pin']).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.progress != QuestionnaireProgressChoices.NOT_STARTED:
            # create a copy of questionnaire response model if the link has already been
            # accessed by one of the user
            instance.pk = None
            instance._state.adding = True
            instance.save()

        instance.progress = QuestionnaireProgressChoices.IN_PROGRESS
        instance.save()
        serializer = self.get_serializer(instance)

        # we can also redirect to a web url by including instance ID in query parameters
        return Response(serializer.data)
