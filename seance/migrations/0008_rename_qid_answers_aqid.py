# Generated by Django 5.0.3 on 2024-03-18 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0007_questions_alter_answers_qid_delete_subquestions_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='qid',
            new_name='aqid',
        ),
    ]
