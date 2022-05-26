from django.urls import reverse
from graphql_relay import from_global_id, to_global_id

from api.quiz.choices import QuestionnaireProgressChoices
from api.quiz.factories import QuestionnaireResponsesFactory
from api.quiz.schema import QuestionnaireResponsesNode
from api.tests import BaseAPITestCase


class QuestionnaireResponseTestUtils(object):

    @staticmethod
    def get_questionnaire_response_url(pin):
        return reverse('quiz:questionnaire-responses', kwargs={"pin": pin})


class TestQuestionnaireResponse(BaseAPITestCase):
    """
        Test case for fetching Questionnaire Response Details from shared link
    """

    def setUp(self):
        super().setUp()
        self.questionnaire_response = QuestionnaireResponsesFactory.create(
            progress=QuestionnaireProgressChoices.NOT_STARTED)

    def test_questionnaire_response(self):
        response = self.user_client.get(
            QuestionnaireResponseTestUtils.get_questionnaire_response_url(self.questionnaire_response.pin)
        )
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], to_global_id(QuestionnaireResponsesNode.__name__,
                                                  self.questionnaire_response.id))
        self.assertEqual(data['questionnaire']['title'], self.questionnaire_response.questionnaire.title)
        self.assertEqual(from_global_id(data['questionnaire']['id'])[1],
                         str(self.questionnaire_response.questionnaire.id))

    def test_questionnaire_response_copy(self):
        self.questionnaire_response.progress = QuestionnaireProgressChoices.IN_PROGRESS
        self.questionnaire_response.save()

        response = self.user_client.get(
            QuestionnaireResponseTestUtils.get_questionnaire_response_url(self.questionnaire_response.pin)
        )
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertNotEqual(data['id'], to_global_id(QuestionnaireResponsesNode.__name__,
                                                     self.questionnaire_response.id))
        self.assertEqual(data['questionnaire']['title'], self.questionnaire_response.questionnaire.title)
        self.assertEqual(from_global_id(data['questionnaire']['id'])[1],
                         str(self.questionnaire_response.questionnaire.id))
