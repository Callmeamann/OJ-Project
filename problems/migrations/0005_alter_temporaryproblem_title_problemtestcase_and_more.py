# Generated by Django 5.0.6 on 2024-07-05 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_temporaryproblem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryproblem',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='ProblemTestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.TextField()),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='problem_test_cases', to='problems.problem')),
                ('temporary_problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='problems.temporaryproblem')),
            ],
        ),
        migrations.CreateModel(
            name='TestCaseExpectedOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.TextField()),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_expected_outputs', to='problems.problemtestcase')),
            ],
        ),
    ]
