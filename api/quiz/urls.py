from django.urls import path

from api.quiz.views import QuestionnaireResponsesRetrieveView

app_name = "quiz"


urlpatterns = [
    # Questionnaire Answers
    path(
        "<str:pin>/",
        QuestionnaireResponsesRetrieveView.as_view(),
        name="questionnaire-responses"
    ),
]
