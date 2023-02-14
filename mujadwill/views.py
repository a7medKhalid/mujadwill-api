from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db.models import Sum



from .helpers.Imports import importSectionsFunction
from .helpers.Imports import importInstructorsFunction

from .helpers.GeneticAlgorithm import GeneticAlgorithmClass
from .helpers.Fitness import FitnessEnum

from .helpers.Mail import sendPrefrncesEmail



from .models import *
from .serializers import *
from random import randint
from datetime import datetime

class import_sections(APIView):
    
    # upload sections csv file
    def post(self, request, format=None):

        # drop all sections
        Section.objects.all().delete()
        importSectionsFunction(request.FILES['file'])
        return Response(status=status.HTTP_201_CREATED)

class import_instructors(APIView):
    
    # upload instructors csv file
    def post(self, request, format=None):
        
        # drop all instructors
        Instructor.objects.all().delete()
        importInstructorsFunction(request.FILES['file'])

        # send email to all instructors
        sendPrefrncesEmail()

        return Response(status=status.HTTP_201_CREATED)

class generate_schedules(APIView):

    # generate schedules
    def post(self, request, format=None):

        # drop all schedules
        Schedule.objects.all().delete()

        # get all sections
        sections_list = Section.objects.all()

        # get all instructors
        instructors_list = Instructor.objects.all()

        if len(sections_list) == 0 or len(instructors_list) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Please import sections and instructors first.'})
        
        

        for i in range(0,4):
            
            best_fitness = 0
            best_chromosome = None

            G = GeneticAlgorithmClass()

            # generate population 
            population = G.generatePopulation(sections_list, instructors_list)

            counter = 0
            while True:
                # count fitness
                ranked_population, fitness, conflict_fitness, fulload_fitness, fourDays_fitness, lab_fitness,preffernce_fitness = G.calculateFitness(population)

                # check if the fitness is better than the best fitness
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_chromosome = population
                    best_conflict_fitness = conflict_fitness
                    best_fullLoad_fitness = fulload_fitness 
                    best_fourDays_fitness = fourDays_fitness
                    best_lab_fitness = lab_fitness
                    best_preffernce_fitness = preffernce_fitness

                    
                # check if the fitness is 100%
                # if fitness == (3 * len(sections_list)):
                #     break

                # crossover
                population = G.crossover(ranked_population, instructors_list)

                if population == None:
                    break

                counter += 1

                if counter == 1000:
                    break

            # best_fitness = best_fitness / ((FitnessEnum.CONFLICT.value + FitnessEnum.FULL_LOAD.value + FitnessEnum.FOUR_DAYS.value) * len(sections_list))
            best_conflict_fitness = best_conflict_fitness / (FitnessEnum.CONFLICT.value * len(sections_list))
            best_fullLoad_fitness = best_fullLoad_fitness / (FitnessEnum.FULL_LOAD.value * len( sections_list))
            best_fourDays_fitness = best_fourDays_fitness / (FitnessEnum.FOUR_DAYS.value * len(sections_list))
            lab_sections_count = Section.objects.filter(is_theory=0).count()
            best_lab_fitness = best_lab_fitness / (FitnessEnum.LAB.value * lab_sections_count)
            best_preffernce_fitness = best_preffernce_fitness / (FitnessEnum.PREFERENCE.value * len(sections_list))

            best_fitness = ((best_conflict_fitness * FitnessEnum.CONFLICT.value) + (best_fullLoad_fitness * FitnessEnum.FULL_LOAD.value) + (best_fourDays_fitness * FitnessEnum.FOUR_DAYS.value) + (best_lab_fitness * FitnessEnum.LAB.value) + (best_preffernce_fitness * FitnessEnum.PREFERENCE.value))  / (FitnessEnum.CONFLICT.value + FitnessEnum.FULL_LOAD.value + FitnessEnum.FOUR_DAYS.value + FitnessEnum.LAB.value + FitnessEnum.PREFERENCE.value )
            # save the best chromosome as csv file in Schedules folder

            fileName =  'Schedule-' + str(randint(0, 10000)) + '.csv'
            file = open(fileName, 'w', encoding='utf-8-sig')
            file.write('id,course_title,instructor_name,days_type,start_time,end_time,hours,\n')
            for section in best_chromosome:
                file.write(str(section.id) + ',' + str(section.course_title) + ',' + str(section.instructor.name) + ',' + str(section.days_type) + ',' + str(section.start_time) + ',' + str(section.end_time) + ',' + str(section.hours) + '\n')
            file.close()

            schedule = Schedule.objects.create(fileName=fileName, fitness=best_fitness, conflict_fitness=best_conflict_fitness, fullLoad_fitness=best_fullLoad_fitness, fourDays_fitness=best_fourDays_fitness, lab_fitness=best_lab_fitness, preference_fitness=best_preffernce_fitness)
            schedule.save()


        return Response(status=status.HTTP_201_CREATED)

class get_schedules(APIView):
    # get schedules
    def get(self, request, format=None):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class get_schedule(APIView):
    # get schedule
    def get(self, request, id, format=None):
        
        # download the schedule file
        schedule = Schedule.objects.get(id=id)

        if schedule == None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Schedule not found.'})
        fileName = schedule.fileName
        file = open(fileName, 'r')
        response = Response(file.read())
        return response

class get_hours(APIView):
    # get hours
    def get(self, request, format=None):
        sections_hours = Section.objects.all().aggregate(Sum('hours'))
        instructors_hours = Instructor.objects.all().aggregate(Sum('max_hours'))

        return Response({'sections_hours': sections_hours, 'instructors_hours': instructors_hours})

from .models import Preffernce, Instructor
class add_preference(APIView):
    # add preference
    def post(self, request, format=None):
        secret_token = request.data['secret_token']
        instructor = Instructor.objects.get(secret_token=secret_token)

        if Instructor == None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Instructor not found.'})
        
        preference = Preffernce.objects.create(instructor=instructor, prefferd_time=request.data['prefferd_time'], prefferd_days=request.data['prefferd_days'], prefferd_subjects=request.data['prefferd_subjects'])

        preference.save()
        
        return Response(status=status.HTTP_201_CREATED)
