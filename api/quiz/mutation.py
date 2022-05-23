import graphene
from django.db import transaction
from graphene import relay
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from api.quiz.models import Questionnaire, Questions
from api.quiz.schema import QuestionnaireNode


class CreateQuestionsInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    seq_no = graphene.Int()
    type = graphene.Int(required=True)
    choice_options = graphene.List(graphene.String)


class UpdateQuestionsInput(CreateQuestionsInput):
    id = graphene.String()


class CreateQuestionnaire(relay.ClientIDMutation):
    """
        Create a Questionnaire
    """
    class Input:
        title = graphene.String(required=True)
        questions = graphene.List(CreateQuestionsInput)

    questionnaire = graphene.Field(QuestionnaireNode)

    @staticmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(root, info, title, questions):
        questionnaire = Questionnaire.objects.create(title=title, created_by=info.context.user)

        # bulk create questions
        questions_list = [
            Questions(**question_data, questionnaire=questionnaire) for question_data in questions
        ]
        Questions.objects.bulk_create(questions_list)
        return CreateQuestionnaire(questionnaire=questionnaire)


class UpdateQuestionnaire(relay.ClientIDMutation):
    """
        Update a Questionnaire
    """
    class Input:
        id = graphene.ID(required=True)
        questions = graphene.List(UpdateQuestionsInput, required=True)
        title = graphene.String()

    questionnaire = graphene.Field(QuestionnaireNode)

    @staticmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(root, info, id, questions, title=None):
        try:
            questionnaire = Questionnaire.objects.get(id=from_global_id(id)[1])
            if title is not None:
                questionnaire.title = title
                questionnaire.save()

            existing_questions_ids = []
            new_questions_list = []
            for question_data in questions:
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

            return UpdateQuestionnaire(questionnaire=questionnaire)

        except Questionnaire.DoesNotExist:
            raise GraphQLError('Questionnaire object not found')

        except Questions.DoesNotExist:
            raise GraphQLError('Question object not found')


class QuizMutation(graphene.ObjectType):
    create_questionnaire = CreateQuestionnaire.Field()
    update_questionnaire = UpdateQuestionnaire.Field()
