# Generated by Django 4.2.7 on 2023-12-09 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gumfuel', '0003_bodypart_exercise_titles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='titles',
            field=models.ManyToManyField(blank=True, related_name='tags', to='gumfuel.bodypart'),
        ),
    ]
