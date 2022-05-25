from api.managers import BaseQueryManager
from api.quiz.choices import QuestionnaireProgressChoices


class QuestionnaireQueryManager(BaseQueryManager):

    def with_prefetch_related(self, objects='questions'):
        queryset = self
        if not isinstance(objects, list):
            objects = [objects]
        if 'questions' in objects:
            queryset = queryset.prefetch_related('questions')
        return queryset

    def by_user(self, user):
        return self.filter(created_by=user)


class QuestionsQueryManager(BaseQueryManager):

    pass


class AnswersQueryManager(BaseQueryManager):

    pass


class QuestionnaireResponsesQueryManager(BaseQueryManager):

    def with_select_related(self, objects='questionnaire'):
        queryset = self
        if not isinstance(objects, list):
            objects = [objects]
        if 'questionnaire' in objects:
            queryset = queryset.select_related('questionnaire')
        return queryset

    def not_started(self):
        return self.filter(progress=QuestionnaireProgressChoices.NOT_STARTED)

    def with_pin(self, pin):
        return self.filter(pin=pin)
