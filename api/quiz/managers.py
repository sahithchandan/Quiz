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

    def created_by(self, user):
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

    def with_prefetch_related(self, objects='answers'):
        queryset = self
        if not isinstance(objects, list):
            objects = [objects]
        if 'answers' in objects:
            queryset = queryset.prefetch_related('answers')
        if 'questions' in objects:
            queryset = queryset.prefetch_related('answers__question')
        return queryset

    def for_questionnaires(self, questionnaire_ids):
        if not isinstance(questionnaire_ids, list):
            questionnaire_ids = [questionnaire_ids]
        return self.filter(questionnaire_id__in=questionnaire_ids)

    def not_started(self):
        return self.filter(progress=QuestionnaireProgressChoices.NOT_STARTED)

    def with_pin(self, pin):
        return self.filter(pin=pin)

    def created_by(self, user):
        return self.filter(created_by=user)

    def answered_by(self, email):
        return self.filter(answered_by=email)
