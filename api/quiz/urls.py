from django.urls import path

from api.quiz.views import QuestionnaireRetrieveView

app_name = "quiz"


urlpatterns = [
    # Questionnaire
    path("questionnaire/<uuid:pk>/", QuestionnaireRetrieveView.as_view(), name="questionnaire"),
]
