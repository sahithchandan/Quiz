from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from api.models import TimestampedAbstractModel
from api.quiz.choices import QuestionnaireProgressChoices, QuestionTypeChoices
from api.quiz.managers import (
    QuestionnaireQueryManager,
    QuestionsQueryManager,
    AnswersQueryManager,
    QuestionnaireResponsesQueryManager
)
from api.users.models import User


class Questionnaire(TimestampedAbstractModel):
    """
        Model representing Questionnaires
    """
    title = models.CharField(max_length=255)

    # relations
    created_by = models.ForeignKey(User, related_name='questionnaires', on_delete=models.SET_NULL, null=True)

    # filters
    filter = QuestionnaireQueryManager.as_manager()

    class Meta:
        verbose_name_plural = "Questionnaire"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title


class Questions(TimestampedAbstractModel):
    """
        Model representing Questions
    """
    title = models.TextField()
    seq_no = models.PositiveSmallIntegerField(default=1)
    type = models.PositiveSmallIntegerField(choices=QuestionTypeChoices.choices)

    # choices for checkboxes, multiple choices and dropdown questions
    choice_options = ArrayField(models.CharField(max_length=255), null=True, blank=True)

    # relations
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE)

    # filters
    filter = QuestionsQueryManager.as_manager()

    class Meta:
        verbose_name_plural = "Questions"
        indexes = [
            models.Index(fields=['title', 'seq_no'])
        ]
        ordering = ['seq_no']

    def __str__(self):
        return self.title


class Answers(TimestampedAbstractModel):
    """
        Model representing Answers for Questions
    """
    # choices for checkboxes, multiple choices and dropdown questions
    choice = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    free_text = models.TextField(blank=True)

    # relations
    question = models.ForeignKey(Questions, related_name='answers', on_delete=models.CASCADE)

    # filters
    filter = AnswersQueryManager.as_manager()

    class Meta:
        verbose_name_plural = "Answers"
        ordering = ['-created_at']

    def __str__(self):
        return self.question.title


class QuestionnaireResponses(TimestampedAbstractModel):
    """
        Model representing responses of a Questionnaire
    """
    pin = models.CharField(unique=True, max_length=6)
    progress = models.PositiveSmallIntegerField(choices=QuestionnaireProgressChoices.choices,
                                                default=QuestionnaireProgressChoices.NOT_STARTED)
    answered_by = models.EmailField(max_length=255, blank=True, null=True)

    # relations
    questionnaire = models.ForeignKey(Questionnaire, related_name='questionnaire_user_answers',
                                      on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answers, related_name='questionnaire_user_answers', blank=True)

    # filters
    filter = QuestionnaireResponsesQueryManager.as_manager()

    class Meta:
        verbose_name_plural = "Questionnaire Responses"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pin'])
        ]

    def __str__(self):
        return self.questionnaire.title

    @property
    def sharable_link(self):
        # can use a url shortener here
        url = reverse('quiz:questionnaire-responses', kwargs={"pin": self.pin})
        return settings.API_BASE_URL + url
