# Generated by Django 4.1.6 on 2023-02-12 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mujadwill', '0008_section_theory_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='lab_fitness',
            field=models.FloatField(default=0),
        ),
    ]
