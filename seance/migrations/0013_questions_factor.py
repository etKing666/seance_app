# Generated by Django 5.0.3 on 2024-03-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0012_questions_children_questions_parent_questions_step_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='factor',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
