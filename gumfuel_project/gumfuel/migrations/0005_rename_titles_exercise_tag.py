# Generated by Django 4.2.7 on 2023-12-09 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gumfuel', '0004_alter_exercise_titles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='titles',
            new_name='tag',
        ),
    ]