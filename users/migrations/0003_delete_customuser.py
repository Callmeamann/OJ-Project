# Generated by Django 5.0.6 on 2024-06-20 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_bio'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
