from django.db.models.signals import pre_save
from django.dispatch import receiver

from api.quiz.models import QuestionnaireResponses
from api.utils import generate_pin


@receiver(pre_save, sender=QuestionnaireResponses)
def questionnaire_responses(sender, instance, **kwargs):
    instance.pin = generate_pin()
