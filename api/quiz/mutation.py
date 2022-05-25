import graphene
from django.db import transaction
from graphene import relay
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from api.utils import get_object, filter_objects, generate_pin
from api.quiz.models import Questionnaire, Questions, QuestionnaireResponses, Answers
from api.quiz.schema import QuestionnaireNode, QuestionnaireResponsesNode
from api.quiz.choices import QuestionnaireProgressChoices, QuestionTypeChoices


class CreateQuestionsInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    seq_no = graphene.Int()
    type = graphene.Int(required=True)
    choice_options = graphene.List(graphene.String)


class UpdateQuestionsInput(CreateQuestionsInput):
    id = graphene.String()
    title = graphene.String()
    type = graphene.Int()


class AnswersInput(graphene.InputObjectType):
    choice = graphene.List(graphene.String)
    free_text = graphene.String()


class QuestionAnswersInput(graphene.InputObjectType):
    id = graphene.String()
    answer = graphene.Field(AnswersInput)


class CreateQuestionnaire(relay.ClientIDMutation):
    """
        Create a Questionnaire
    """
    class Input:
        title = graphene.String(required=True)
        questions = graphene.List(CreateQuestionsInput)

    @staticmethod
    def validate_questions(questions_data):
        for question_data in questions_data:
            if question_data['type'] not in QuestionTypeChoices.values:
                raise GraphQLError('Invalid question type')

    questionnaire = graphene.Field(QuestionnaireNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **data):
        cls.validate_questions(data['questions'])
        questionnaire = Questionnaire.objects.create(title=data['title'], created_by=info.context.user)

        # bulk create questions
        questions_list = [
            Questions(**question_data, questionnaire=questionnaire) for question_data in data['questions']
        ]
        Questions.objects.bulk_create(questions_list)
        return cls(questionnaire=questionnaire)


class UpdateQuestionnaire(relay.ClientIDMutation):
    """
        Update a Questionnaire
    """
    class Input:
        id = graphene.String(required=True)
        questions = graphene.List(UpdateQuestionsInput, required=True)
        title = graphene.String()

    questionnaire = graphene.Field(QuestionnaireNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            questionnaire = get_object(Questionnaire, data['id'])
            if data.get('title') is not None:
                questionnaire.title = data['title']
                questionnaire.save()

            existing_questions_ids = []
            new_questions_list = []
            for question_data in data['questions']:

                if 'id' in question_data:
                    # update existing question
                    question_id = from_global_id(question_data.pop('id'))[1]
                    Questions.objects.filter(id=question_id).update(**question_data)
                    existing_questions_ids.append(question_id)
                else:
                    # add to new questions list for bulk create
                    new_questions_list.append(
                        Questions(**question_data, questionnaire=questionnaire)
                    )

            # delete questions that are not included in the data
            questionnaire.questions.exclude(id__in=existing_questions_ids).delete()

            if new_questions_list:
                # bulk create new questions if present in the data
                Questions.objects.bulk_create(new_questions_list)

            return cls(questionnaire=questionnaire)

        except Questionnaire.DoesNotExist:
            raise GraphQLError('Questionnaire object not found')

        except Questions.DoesNotExist:
            raise GraphQLError('Question object not found')


class CreateQuestionnaireResponses(relay.ClientIDMutation):
    """
        Create a QuestionnaireResponses for sharing a Questionnaire
    """
    class Input:
        questionnaire_id = graphene.String(required=True)

    questionnaire_response = graphene.Field(QuestionnaireResponsesNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **data):
        questionnaire = get_object(Questionnaire, data['questionnaire_id'])
        if not questionnaire:
            raise GraphQLError("Questionnaire not found")
        questionnaire_response = QuestionnaireResponses.objects.create(pin=generate_pin(),
                                                                       questionnaire=questionnaire)
        return CreateQuestionnaireResponses(questionnaire_response=questionnaire_response)


class CreateUserAnswers(relay.ClientIDMutation):
    """
        Create a User Answers for a Questionnaire
    """
    class Input:
        questionnaire_user_answers_id = graphene.String(required=True)
        questions = graphene.List(QuestionAnswersInput, required=True)
        email = graphene.String()

    questionnaire_user_answers = graphene.Field(QuestionnaireResponsesNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **data):
        questionnaire_user_answers = get_object(QuestionnaireResponses, data['questionnaire_user_answers_id'])
        if questionnaire_user_answers.progress == QuestionnaireProgressChoices.COMPLETED:
            raise GraphQLError('You have already submitted the questionnaire')

        # answers data for bulk creating the Answers
        answers_data = [
            {'question_id': from_global_id(question['id'])[1],
             "choice": question['answer'].get('choice'),
             "free_text": question['answer'].get('free_text')} for question in data['questions']
        ]
        answers = Answers.objects.bulk_create([Answers(**answer_data) for answer_data in answers_data])

        # set answers for the unique questionnaire link
        questionnaire_user_answers.answers.set(answers)
        questionnaire_user_answers.progress = QuestionnaireProgressChoices.COMPLETED
        questionnaire_user_answers.answered_by = data.get('email')
        questionnaire_user_answers.save()
        return cls(questionnaire_user_answers=None)


class DeleteQuestionnaire(relay.ClientIDMutation):
    """
        Deleting a Questionnaire
    """
    class Input:
        questionnaire_id = graphene.String(required=True)

    questionnaire = graphene.Field(QuestionnaireNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **data):
        questionnaire = filter_objects(Questionnaire, data['questionnaire_id']).by_user(info.context.user).first()
        if not questionnaire:
            raise GraphQLError('You do not have permission to delete the questionnaire')

        # delete questionnaire
        questionnaire.delete()
        return cls(questionnaire=None)


class QuizMutation(graphene.ObjectType):

    # questionnaire
    create_questionnaire = CreateQuestionnaire.Field()
    update_questionnaire = UpdateQuestionnaire.Field()
    delete_questionnaire = DeleteQuestionnaire.Field()

    # referral link
    create_questionnaire_response = CreateQuestionnaireResponses.Field()

    # answers
    create_user_answers = CreateUserAnswers.Field()
