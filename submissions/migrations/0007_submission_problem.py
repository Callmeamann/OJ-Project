# Generated by Django 5.0.6 on 2024-07-12 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0010_alter_problem_difficulty'),
        ('submissions', '0006_alter_expectedoutput_test_case_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.problem'),
        ),
    ]
