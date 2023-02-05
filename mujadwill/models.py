from django.db import models

# Create your models here.

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    max_hours = models.IntegerField()

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
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.course_symbol + " " + self.section


