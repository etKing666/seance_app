# Generated by Django 5.0.3 on 2024-03-19 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0011_alter_answers_aqid'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='children',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='questions',
            name='parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questions',
            name='step',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='questions',
            name='section',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
