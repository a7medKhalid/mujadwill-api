# Generated by Django 4.1.6 on 2023-02-13 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mujadwill', '0010_instructor_university_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='section',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
