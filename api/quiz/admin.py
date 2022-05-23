from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from api.quiz import models


class QuestionsInline(admin.TabularInline):
    model = models.Questions


@admin.register(models.Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    inlines = [QuestionsInline]


@admin.register(models.Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "type"]
    list_filter = ["type"]


@admin.register(models.QuestionnaireUserAnswers)
class QuestionnaireUserAnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "get_questionnaire_title", "progress"]
    list_filter = ["progress"]

    @admin.display(description="Questionnaire", ordering='questionnaire__title')
    def get_questionnaire_title(self, obj):
        url = reverse("admin:quiz_questionnaire_change", args=[obj.questionnaire.id])
        link = '<a href="%s">%s</a>' % (url, obj.questionnaire.title)
        return mark_safe(link)


@admin.register(models.Answers)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "get_question_title", "choice", "free_text"]

    @admin.display(description="Question", ordering='question__title')
    def get_question_title(self, obj):
        url = reverse("admin:quiz_questions_change", args=[obj.question.id])
        link = '<a href="%s">%s</a>' % (url, obj.question.title)
        return mark_safe(link)
