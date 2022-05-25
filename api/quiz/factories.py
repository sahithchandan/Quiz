import factory.fuzzy

from api.quiz.choices import QuestionTypeChoices, QuestionnaireProgressChoices
from api.quiz.models import Questionnaire, Questions, Answers, QuestionnaireResponses


class QuestionnaireFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()

    class Meta:
        model = Questionnaire


class QuestionsFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    seq_no = factory.fuzzy.FuzzyInteger(low=1, high=100)
    type = factory.fuzzy.FuzzyChoice(QuestionTypeChoices.choices, getter=lambda c: c[0])

    # relations
    questionnaire = factory.SubFactory(QuestionnaireFactory)

    class Meta:
        model = Questions


class AnswersFactory(factory.django.DjangoModelFactory):

    question = factory.SubFactory(QuestionsFactory)

    class Meta:
        model = Answers


class QuestionnaireResponsesFactory(factory.django.DjangoModelFactory):
    pin = factory.fuzzy.FuzzyText(length=6)
    progress = factory.fuzzy.FuzzyChoice(QuestionnaireProgressChoices.choices, getter=lambda c: c[0])

    # relations
    questionnaire = factory.SubFactory(QuestionnaireFactory)

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of areas were passed in, use them
            for answer in extracted:
                self.answers.add(answer)

    class Meta:
        model = QuestionnaireResponses
