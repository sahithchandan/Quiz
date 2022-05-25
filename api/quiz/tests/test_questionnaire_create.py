
import json

from api.tests import BaseGraphQLTestCase


class QuestionnaireCreateGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for Questionnaire Create
    """

    def setUp(self):
        super().setUp()

    @staticmethod
    def get_query():
        return '''
            mutation CreateQuestionnaire{
              createQuestionnaire(
                input: {
                  title: "All About Earth",
                  questions: [
                      {
                        title: "What is the shape of the Earth?",
                        type: 0,
                        seqNo: 1
                      },
                      {
                        title: "Is there life on Earth?",
                        type: 0,
                        seqNo: 2
                      },
                      {
                          title: "Which of this is not a continent?",
                          type: 3,
                          choiceOptions: [
                              "Asia",
                              "Africa",
                              "America",
                              "Australia"
                          ]
                      },
                      {
                          title: "Choose all oceans",
                          type: 2,
                          choiceOptions: [
                              "Indian",
                              "Pacific",
                              "Atlantic",
                              "Caribbean"
                          ]
                      },
                      {
                          title: "Is Pluto a part of solar system?",
                          type: 4,
                          choiceOptions: [
                              "Yes",
                              "No"
                          ]
                      }
                    ]
                }){
                questionnaire{
                  id,
                  title
                }
              }
            }
            '''

    def test_questionnaire_create(self):
        response = self.query(
            self.get_query(),
            op_name='CreateQuestionnaire',
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertIn('id', data['createQuestionnaire']['questionnaire'])

    def test_questionnaire_create_invalid_question_type(self):
        query = '''
            mutation CreateQuestionnaire{
              createQuestionnaire(
                input: {
                  title: "All About Earth",
                  questions: [
                      {
                        title: "What is the shape of the Earth?",
                        type: 5,
                        seqNo: 1
                      }
                    ]
                }){
                questionnaire{
                  id,
                  title
                }
              }
            }
            '''
        response = self.query(
            query,
            op_name='CreateQuestionnaire',
            headers={"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        )
        self.assertResponseHasErrors(response)
