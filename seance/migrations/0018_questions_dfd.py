# Generated by Django 5.0.3 on 2024-04-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0017_suggestions_risk_suggestions_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='dfd',
            field=models.BooleanField(default=False),
        ),
    ]
