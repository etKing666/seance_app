# Generated by Django 5.0.3 on 2024-03-18 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0010_answers_user_alter_users_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='aqid',
            field=models.IntegerField(),
        ),
    ]