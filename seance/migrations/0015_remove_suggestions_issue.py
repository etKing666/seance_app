# Generated by Django 5.0.3 on 2024-03-25 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0014_suggestions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestions',
            name='issue',
        ),
    ]