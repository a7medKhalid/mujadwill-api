# Generated by Django 4.1.6 on 2023-02-13 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mujadwill', '0012_section_hours'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preffernce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefferd_time', models.CharField(max_length=10)),
                ('prefferd_days', models.CharField(max_length=10)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preffernces', to='mujadwill.instructor')),
            ],
        ),
    ]
