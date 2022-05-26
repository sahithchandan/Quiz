import json

from graphql_relay import to_global_id

from api.quiz.factories import QuestionnaireFactory, QuestionnaireResponsesFactory
from api.quiz.schema import QuestionnaireNode, QuestionnaireResponsesNode
from api.tests import BaseGraphQLTestCase


class SharableLinkCreateGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for creating a sharable link
    """

    def setUp(self):
        super().setUp()
        self.questionnaire = QuestionnaireFactory.create()

    @staticmethod
    def get_query():
        return '''
            mutation createQuestionnaireResponse ($input: CreateQuestionnaireResponsesInput!) {
              createQuestionnaireResponse (input: $input){
                questionnaireResponse{
                  id,
                  sharableLink
                }
              }
            }
            '''

    def test_create_sharable_link(self):
        response = self.query(
            self.get_query(),
            op_name='createQuestionnaireResponse',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            input_data={'questionnaireId': to_global_id(QuestionnaireNode.__name__, self.questionnaire.id)}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertIn('sharableLink', data['createQuestionnaireResponse']['questionnaireResponse'])

    def test_fetch_existing_sharable_link(self):
        questionnaire_response = QuestionnaireResponsesFactory(questionnaire=self.questionnaire,
                                                               created_by=self.user)
        response = self.query(
            self.get_query(),
            op_name='createQuestionnaireResponse',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            input_data={'questionnaireId': to_global_id(QuestionnaireNode.__name__, self.questionnaire.id)}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertIn('sharableLink', data['createQuestionnaireResponse']['questionnaireResponse'])
        self.assertEqual(data['createQuestionnaireResponse']['questionnaireResponse']['id'],
                         to_global_id(QuestionnaireResponsesNode.__name__, questionnaire_response.id))
