# Generated by Django 3.2.13 on 2022-05-26 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaireresponses',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who chooses to share the questionnaire', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questionnaire_responses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answers',
            name='free_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireresponses',
            name='answers',
            field=models.ManyToManyField(blank=True, related_name='questionnaire_responses', to='quiz.Answers'),
        ),
        migrations.AlterField(
            model_name='questionnaireresponses',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire_responses', to='quiz.questionnaire'),
        ),
    ]