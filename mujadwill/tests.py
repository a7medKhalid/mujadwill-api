from django.test import TestCase
from .models import Section, Instructor, Schedule

class TestGenrateSchedules(TestCase):

    def setUp(self):
        # add sections to the database
        s = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=True, course_title='Software Engineering', start_time=8, end_time=10, days_type='SAT')
        l = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=False, course_title='Software Engineering', start_time=11, end_time=12, days_type='SAT', theory_section=s)
        s.save()
        l.save()
        # add instructors to the database
        i = Instructor.objects.create(name='Ahmed', max_hours=20, university_id='1234')
        i.save()

    def test_generate_schedules(self):
        
        response = self.client.post('/api/generate-schedules/')
        self.assertEqual(response.status_code, 201)

        schedule = Schedule.objects.first()
        print('fitness: ', schedule.fitness, 'conflict_fitness: ', schedule.conflict_fitness, 'fullLoad_fitness: ', schedule.fullLoad_fitness, 'fourDays_fitness: ', schedule.fourDays_fitness, 'lab_fitness: ', schedule.lab_fitness)
        self.assertEqual(schedule.fitness, 1.0)
        self.assertEqual(schedule.conflict_fitness, 1.0)
        self.assertEqual(schedule.fullLoad_fitness, 1.0)
        self.assertEqual(schedule.fourDays_fitness, 1.0)
        self.assertEqual(schedule.lab_fitness, 1.0)


    # def test_schedule_fitness(self):

        

    

        