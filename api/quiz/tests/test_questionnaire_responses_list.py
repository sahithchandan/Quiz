import json

from api.quiz.factories import QuestionnaireFactory, QuestionnaireResponsesFactory, AnswersFactory, QuestionsFactory
from api.tests import BaseGraphQLTestCase
from api.users.factories import UserFactory


class QuestionnaireResponseAnswersListGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for Fetching all responses of Questionnaire
    """

    def setUp(self):
        self.user = UserFactory()
        super().setUp(self.user)
        self.questionnaires = QuestionnaireFactory.create_batch(2)
        QuestionsFactory.create_batch(15, questionnaire=self.questionnaires[0])
        QuestionnaireResponsesFactory(questionnaire=self.questionnaires[0],
                                      answers=AnswersFactory.create_batch(10),
                                      created_by=self.user)
        QuestionnaireResponsesFactory(questionnaire=self.questionnaires[1],
                                      answers=AnswersFactory.create_batch(20),
                                      created_by=self.user)

    @staticmethod
    def get_query():
        return '''
            query allQuestionnaireResponses ($first: Int = 10, $after: String){
              allQuestionnaireResponses (first: $first, after: $after){
                totalCount,
                edgeCount
                edges {
                  node {
                    id,
                    totalQuestions,
                    totalAnswers,
                    questionnaire {
                      id,
                      title
                    }
                  },
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
            '''

    def test_questionnaire_responses_list(self):
        response = self.query(
            self.get_query(),
            op_name='allQuestionnaireResponses',
            variables={'first': 5},
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertEqual(data['allQuestionnaireResponses']['totalCount'], 2)
        self.assertIn('pageInfo', data['allQuestionnaireResponses'])
        for questionnaire_response in data['allQuestionnaireResponses']['edges']:
            if questionnaire_response['node']['questionnaire']['title'] == self.questionnaires[0].title:
                self.assertEqual(questionnaire_response['node']['totalQuestions'], 15)
                self.assertEqual(questionnaire_response['node']['totalAnswers'], 10)
