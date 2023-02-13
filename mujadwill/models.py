from django.db import models

# Create your models here.

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    max_hours = models.IntegerField()
    university_id =models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Section(models.Model):
    course_symbol = models.CharField(max_length=10)
    course_id = models.IntegerField()
    section = models.CharField(max_length=10)
    is_theory = models.BooleanField()
    course_title = models.CharField(max_length=100)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    days_type = models.CharField(max_length=10)
    theory_section = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='+')


    def __str__(self):
        return self.course_symbol + " " + self.section

class Schedule(models.Model):
    fileName = models.CharField(max_length=100)
    isAccepted = models.BooleanField(default=False)
    fitness = models.FloatField(default=0)
    conflict_fitness = models.FloatField(default=0)
    fullLoad_fitness = models.FloatField(default=0)
    fourDays_fitness = models.FloatField(default=0)
    lab_fitness = models.FloatField(default=0)

