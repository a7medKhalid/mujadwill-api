# Generated by Django 4.1.6 on 2023-02-14 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mujadwill', '0015_instructor_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='preference_fitness',
            field=models.FloatField(default=0),
        ),
    ]
