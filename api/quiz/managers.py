from api.managers import BaseQueryManager


class QuestionnaireQueryManager(BaseQueryManager):

    def with_prefetch_related(self, objects='questions'):
        queryset = self
        if not isinstance(objects, list):
            objects = [objects]
        if 'questions' in objects:
            queryset = queryset.prefetch_related('questions')
        return queryset


class QuestionsQueryManager(BaseQueryManager):

    pass


class AnswersQueryManager(BaseQueryManager):

    pass


class QuestionnaireUserAnswersQueryManager(BaseQueryManager):

    pass
