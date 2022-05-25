
import json

from api.quiz.factories import QuestionnaireFactory
from api.tests import BaseGraphQLTestCase


class QuestionnaireListGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for Questionnaire List
    """

    def setUp(self):
        super().setUp()
        self.questionnaire = QuestionnaireFactory.create_batch(20)

    @staticmethod
    def get_query():
        return '''
            query AllQuestionnaires($first: Int = 10, $after: String, $byMe: Boolean) {
                allQuestionnaires (first: $first, after: $after, byMe: $byMe) {
                  totalCount,
                  edgeCount,
                  edges {
                      node {
                          id,
                          title
                      }
                      cursor
                  },
                  pageInfo{
                      startCursor,
                      endCursor,
                      hasNextPage,
                      hasPreviousPage
                  }
                }
            }
            '''

    def test_questionnaire_list(self):
        response = self.query(
            self.get_query(),
            op_name='AllQuestionnaires',
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']

        self.assertEqual(data['allQuestionnaires']['totalCount'], 20)
        self.assertEqual(data['allQuestionnaires']['edgeCount'], 10)

    def test_questionnaire_list_by_me(self):
        QuestionnaireFactory.create(created_by=self.user)

        response = self.query(
            self.get_query(),
            op_name='AllQuestionnaires',
            variables={'byMe': True},
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']

        self.assertEqual(data['allQuestionnaires']['totalCount'], 1)
        self.assertEqual(data['allQuestionnaires']['edgeCount'], 1)

    def test_questionnaire_paginated_list(self):
        response1 = self.query(
            self.get_query(),
            op_name='AllQuestionnaires',
            variables={'first': 15},
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseNoErrors(response1)
        data1 = json.loads(response1.content)['data']

        self.assertEqual(data1['allQuestionnaires']['totalCount'], 20)
        self.assertEqual(data1['allQuestionnaires']['edgeCount'], 15)

        response2 = self.query(
            self.get_query(),
            op_name='AllQuestionnaires',
            variables={'first': 15,
                       'after': data1['allQuestionnaires']['pageInfo']['endCursor']},
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        data2 = json.loads(response2.content)['data']

        self.assertEqual(data2['allQuestionnaires']['totalCount'], 20)
        self.assertEqual(data2['allQuestionnaires']['edgeCount'], 5)
