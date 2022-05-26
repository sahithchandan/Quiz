
import json

from graphql_relay import to_global_id

from api.quiz.factories import QuestionnaireFactory, QuestionsFactory
from api.quiz.schema import QuestionnaireNode
from api.tests import BaseGraphQLTestCase


class QuestionnaireListGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for Questionnaire List
    """

    def setUp(self):
        super().setUp()
        self.questionnaire = QuestionnaireFactory.create()
        self.questions = QuestionsFactory.create_batch(20, questionnaire=self.questionnaire)

    @staticmethod
    def get_query():
        return '''
            query Questionnaire($id: ID!, $first: Int = 10, $after: String) {
                questionnaire(id: $id){
                    id,
                    title,
                    questions (first: $first, after: $after){
                        totalCount,
                        edgeCount,
                        edges {
                            node {
                                id,
                                title,
                                seqNo,
                                type,
                                choiceOptions
                            },
                            cursor
                        },
                        pageInfo {
                            startCursor,
                            endCursor,
                            hasNextPage,
                            hasPreviousPage
                        }
                    }
                }
            }
            '''

    def test_questionnaire_details(self):
        questionnaire_id = to_global_id(QuestionnaireNode.__name__, self.questionnaire.id)
        response = self.query(
            self.get_query(),
            op_name='Questionnaire',
            variables={"id": questionnaire_id},
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertEqual(data['questionnaire']['id'], questionnaire_id)
        self.assertEqual(data['questionnaire']['questions']['totalCount'], 20)
