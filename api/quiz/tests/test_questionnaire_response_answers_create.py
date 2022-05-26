import json

from graphql_relay import to_global_id

from api.quiz.choices import QuestionnaireProgressChoices
from api.quiz.factories import QuestionnaireFactory, QuestionnaireResponsesFactory, QuestionsFactory
from api.quiz.models import QuestionnaireResponses
from api.quiz.schema import QuestionnaireResponsesNode, QuestionsNode
from api.tests import BaseGraphQLTestCase


class QuestionnaireResponseAnswersGraphQLTest(BaseGraphQLTestCase):
    """
        Test case for submitting answers of a questionnaire
    """

    def setUp(self):
        super().setUp()
        self.questionnaire = QuestionnaireFactory.create()
        self.questions = QuestionsFactory.create_batch(5, questionnaire=self.questionnaire)
        self.questionnaire_response = QuestionnaireResponsesFactory.create(
            progress=QuestionnaireProgressChoices.IN_PROGRESS,
            questionnaire=self.questionnaire
        )

    @staticmethod
    def get_query():
        return '''
            mutation createQuestionnaireResponseAnswers ($input: CreateQuestionnaireResponseAnswersInput!) {
              createQuestionnaireResponseAnswers (input: $input){
                questionnaireResponse{
                    id
                }
              }
            }
            '''

    def test_create_questionnaire_response_answers(self):
        data_input = {
            'questionnaireResponseId': to_global_id(QuestionnaireResponsesNode.__name__,
                                                    self.questionnaire_response.id),
            'questions': [
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[0].id),
                    'answer': {
                        'choice': [
                            'a'
                        ]
                    }
                },
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[1].id),
                    'answer': {
                        'choice': [
                            'b'
                        ]
                    }
                },
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[2].id),
                    'answer': {
                        'freeText': "test answer"
                    }
                },
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[3].id),
                    'answer': {
                        'freeText': "test answer 2"
                    }
                }
            ],
            'email': "test@test.com"
        }
        response = self.query(
            self.get_query(),
            op_name='createQuestionnaireResponseAnswers',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            input_data=data_input
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']
        self.assertIsNone(data['createQuestionnaireResponseAnswers']['questionnaireResponse'])

        questionnaire_response = QuestionnaireResponses.filter.with_ids(self.questionnaire_response.id).first()
        self.assertEqual(questionnaire_response.progress, QuestionnaireProgressChoices.COMPLETED)
        self.assertEqual(questionnaire_response.answered_by, "test@test.com")

    def test_create_questionnaire_response_answers_duplicate(self):
        self.questionnaire_response.answered_by = self.user.email
        self.questionnaire_response.save()
        data_input = {
            'questionnaireResponseId': to_global_id(QuestionnaireResponsesNode.__name__,
                                                    self.questionnaire_response.id),
            'questions': [
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[0].id),
                    'answer': {
                        'choice': [
                            'a'
                        ]
                    }
                },
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[1].id),
                    'answer': {
                        'choice': [
                            'b'
                        ]
                    }
                },
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[2].id),
                    'answer': {
                        'freeText': "test answer"
                    }
                },
                {
                    'id': to_global_id(QuestionsNode.__name__, self.questions[3].id),
                    'answer': {
                        'freeText': "test answer 2"
                    }
                }
            ],
            'email': self.user.email
        }
        response = self.query(
            self.get_query(),
            op_name='createQuestionnaireResponseAnswers',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            input_data=data_input
        )
        self.assertResponseHasErrors(response)
