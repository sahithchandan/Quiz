from django.urls import path

from api.quiz.views import QuestionnaireUserAnswersRetrieveView

app_name = "quiz"


urlpatterns = [
    # Questionnaire Answers
    path(
        "questionnaire_user_answers/<uuid:pk>/",
        QuestionnaireUserAnswersRetrieveView.as_view(),
        name="questionnaire-user-answers"
    ),
]
