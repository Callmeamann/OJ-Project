# Generated by Django 5.0.6 on 2024-07-06 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_alter_temporaryproblem_title_problemtestcase_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcaseexpectedoutput',
            name='test_case',
        ),
        migrations.CreateModel(
            name='TemporaryTestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.TextField()),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='problem_test_cases', to='problems.problem')),
                ('temporary_problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temporary_test_cases', to='problems.temporaryproblem')),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryExpectedOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.TextField()),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_expected_outputs', to='problems.temporarytestcase')),
            ],
        ),
        migrations.DeleteModel(
            name='ProblemTestCase',
        ),
        migrations.DeleteModel(
            name='TestCaseExpectedOutput',
        ),
    ]
