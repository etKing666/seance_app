# Generated by Django 5.0.3 on 2024-03-18 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0009_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='seance.users'),
        ),
        migrations.AlterField(
            model_name='users',
            name='uid',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
