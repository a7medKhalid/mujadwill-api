from django.test import TestCase
from .models import Section, Instructor, Schedule

class TestGenrateSchedules(TestCase):

    def setUp(self):
        # add sections to the database
        s = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=True, course_title='Software Engineering', start_time=800, end_time=1000, days_type='UTR')
        l = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=False, course_title='Software Engineering', start_time=1100, end_time=1200, days_type='UTR', theory_section=s)
        s.save()
        l.save()
        # add instructors to the database
        i = Instructor.objects.create(name='Ahmed', max_hours=20, university_id='1234')
        i.save()

    def test_generate_schedules(self):
        
        response = self.client.post('/api/generate-schedules/')
        self.assertEqual(response.status_code, 201)
        
        schedule = Schedule.objects.first()
        print('fitness: ', schedule.fitness, 'conflict_fitness: ', schedule.conflict_fitness, 'fullLoad_fitness: ', schedule.fullLoad_fitness, 'fourDays_fitness: ', schedule.fourDays_fitness, 'lab_fitness: ', schedule.lab_fitness, 'preference_fitness: ', schedule.preference_fitness)
        self.assertEqual(schedule.fitness, 1.0)
        self.assertEqual(schedule.conflict_fitness, 1.0)
        self.assertEqual(schedule.fullLoad_fitness, 1.0)
        self.assertEqual(schedule.fourDays_fitness, 1.0)
        self.assertEqual(schedule.lab_fitness, 1.0)

class TestGenerateschedulesFailures(TestCase):
    def setUp(self):
        # add sections to the database
        s = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=True, course_title='Software Engineering', start_time=800, end_time=1000, days_type='UTR')
        l = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=False, course_title='Software Engineering', start_time=800, end_time=1000, days_type='UTR', theory_section=s)
        s2 = Section.objects.create(course_symbol='CCSW', course_id=1, section='B', is_theory=True, course_title='Software Engineering', start_time=1200, end_time=1550, days_type='MW')
        s.save()
        l.save()
        s2.save()
        # add instructors to the database
        i = Instructor.objects.create(name='Ahmed', max_hours=5, university_id='1234')
        i.save()

    def test_generate_schedules(self):
        
        response = self.client.post('/api/generate-schedules/')
        self.assertEqual(response.status_code, 201)

        schedule = Schedule.objects.first()
        
        self.assertNotEqual(schedule.fitness, 1.0)
        self.assertNotEqual(schedule.conflict_fitness, 1.0)
        self.assertNotEqual(schedule.fullLoad_fitness, 1.0)
        self.assertNotEqual(schedule.fourDays_fitness, 1.0)



class ApplicationTests(TestCase):

    def setUp(self):
        # add sections to the database
        s = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=True, course_title='Software Engineering', start_time=800, end_time=1000, days_type='UTR')
        l = Section.objects.create(course_symbol='CCSW', course_id=1, section='A', is_theory=False, course_title='Software Engineering', start_time=1100, end_time=1200, days_type='UTR', theory_section=s)
        s.save()
        l.save()
        # add instructors to the database
        i = Instructor.objects.create(name='Ahmed', max_hours=20, university_id='1234')
        i.save()
        # add schedule to the database
        schedule = Schedule.objects.create(fitness=1.0, conflict_fitness=1.0, fullLoad_fitness=1.0, fourDays_fitness=1.0, lab_fitness=1.0)
        schedule.save()

    def test_generate_schedules(self):
        response = self.client.post('/api/generate-schedules/')
        self.assertEqual(response.status_code, 201)

    def test_get_schedules(self):
        response = self.client.get('/api/get-schedules/')
        self.assertEqual(response.status_code, 200)






        

    

        