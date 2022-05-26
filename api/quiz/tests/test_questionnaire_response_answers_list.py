
import json

from graphql_relay import to_global_id

from api.quiz.choices import QuestionnaireProgressChoices
from api.quiz.factories import QuestionnaireFactory, QuestionnaireResponsesFactory, AnswersFactory
from api.quiz.schema import QuestionnaireResponsesNode
from api.tests import BaseGraphQLTestCase
from api.users.factories import UserFactory


class QuestionnaireResponseAnswersListGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for Fetching all responses of Questionnaire
    """

    def setUp(self):
        self.user = UserFactory()
        super().setUp(self.user)
        self.questionnaire = QuestionnaireFactory.create(created_by=self.user)
        self.questionnaire_response = QuestionnaireResponsesFactory(questionnaire=self.questionnaire,
                                                                    answers=AnswersFactory.create_batch(10),
                                                                    progress=QuestionnaireProgressChoices.COMPLETED,
                                                                    created_by=self.user)

    @staticmethod
    def get_query():
        return '''
            query questionnaireResponses($id: ID!, $first: Int = 10, $after: String) {
              questionnaireResponses (id: $id){
                progress,
                answeredBy,
                answers (first: $first, after: $after){
                  totalCount,
                  edgeCount
                  edges {
                    node {
                      question {
                        id,
                        title
                        type,
                      },
                      id,
                      choice,
                      freeText
                    }
                    cursor
                  },
                  pageInfo {
                    hasPreviousPage,
                    hasNextPage,
                    startCursor,
                    endCursor
                  }
                }
              }
            }
            '''

    def test_questionnaire_responses_list(self):
        response = self.query(
            self.get_query(),
            op_name='questionnaireResponses',
            variables={'id': to_global_id(QuestionnaireResponsesNode.__name__, self.questionnaire_response.id),
                       'first': 2},
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertEqual(data['questionnaireResponses']['progress'], QuestionnaireProgressChoices.COMPLETED)
        self.assertEqual(data['questionnaireResponses']['answers']['totalCount'], 10)
        self.assertIn('pageInfo', data['questionnaireResponses']['answers'])
