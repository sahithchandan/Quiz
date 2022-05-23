from django.db import models

from api.quiz import constants


class QuestionnaireProgressChoices(models.IntegerChoices):
    """Class representing Questionnaire progress."""

    NOT_STARTED = 0, constants.NOT_STARTED
    IN_PROGRESS = 1, constants.IN_PROGRESS
    COMPLETED = 2, constants.COMPLETED


class QuestionTypeChoices(models.IntegerChoices):
    """Class representing different version status."""

    SHORT_ANSWER = 0, constants.SHORT_ANSWER
    PARAGRAPH = 1, constants.PARAGRAPH
    CHECKBOXES = 2, constants.CHECKBOXES
    MULTIPLE_CHOICE = 3, constants.MULTIPLE_CHOICE
    DROPDOWN = 4, constants.DROPDOWN
