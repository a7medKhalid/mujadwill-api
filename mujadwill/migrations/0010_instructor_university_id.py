# Generated by Django 4.1.6 on 2023-02-12 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mujadwill', '0009_schedule_lab_fitness'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='university_id',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
