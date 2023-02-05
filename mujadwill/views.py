from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


from .helpers.ImportSections import importSectionsFunction

from .helpers.GeneticAlgorithm import GeneticAlgorithmClass
from .helpers.Fitness import FitnessEnum



from .models import *
from .serializers import *
from random import randint

class upload_sections(APIView):
    
    # upload sections csv file
    def post(self, request, format=None):
        
        importSectionsFunction(request.FILES['file'])
        return Response(status=status.HTTP_201_CREATED)

class generate_schedules(APIView):
    # generate schedules
    def post(self, request, format=None):

        # drop all schedules
        Schedule.objects.all().delete()

        # get all sections
        sections_list = Section.objects.all()

        # get all instructors
        instructors_list = []
        instructors_list.append(Instructor(1, 'محمد', 10))
        instructors_list.append(Instructor(2, 'عبدالله', 10))
        instructors_list.append(Instructor(3, 'علي', 10))
        instructors_list.append(Instructor(4, 'حسن', 10))
        instructors_list.append(Instructor(5, 'زيد', 10))
        instructors_list.append(Instructor(6, 'باسل', 10))
        instructors_list.append(Instructor(7, 'ياسر', 10))
        instructors_list.append(Instructor(8, 'محمود', 10))
        instructors_list.append(Instructor(10, 'وليد', 10))
        instructors_list.append(Instructor(11, 'معاذ', 10))
        instructors_list.append(Instructor(12, 'برقان', 10))
        instructors_list.append(Instructor(13, 'فيصل', 10))
        instructors_list.append(Instructor(14, 'مشاري', 10))
        instructors_list.append(Instructor(15, 'عمر', 10))
        instructors_list.append(Instructor(16, 'عبيد', 10))
        instructors_list.append(Instructor(17, 'حسنين', 10))
        instructors_list.append(Instructor(18, 'مؤيد', 10))
        instructors_list.append(Instructor(19, 'احمد', 10))
        instructors_list.append(Instructor(20, 'فارس', 10))
        instructors_list.append(Instructor(21, 'فراس', 10))

        for i in range(0,4):
            
            best_fitness = 0
            best_chromosome = None

            G = GeneticAlgorithmClass()

            # generate population 
            population = G.generatePopulation(sections_list, instructors_list)

            counter = 0
            while True:
                # count fitness
                ranked_population, fitness, conflict_fitness, fulload_fitness, fourDays_fitness = G.calculateFitness(population)

                # check if the fitness is better than the best fitness
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_chromosome = population
                    best_conflict_fitness = conflict_fitness
                    best_fullLoad_fitness = fulload_fitness 
                    best_fourDays_fitness = fourDays_fitness
                    
                # check if the fitness is 100%
                if fitness == (3 * len(sections_list)):
                    break

                # crossover
                population = G.crossover(ranked_population, instructors_list)

                if population == None:
                    break

                counter += 1

                if counter == 1000:
                    break

            best_fitness = best_fitness / ((FitnessEnum.CONFLICT.value + FitnessEnum.FULL_LOAD.value + FitnessEnum.FOUR_DAYS.value) * len(sections_list))
            best_conflict_fitness = best_conflict_fitness / (FitnessEnum.CONFLICT.value * len(sections_list))
            best_fullLoad_fitness = best_fullLoad_fitness / (FitnessEnum.FULL_LOAD.value * len( sections_list))
            best_fourDays_fitness = best_fourDays_fitness / (FitnessEnum.FOUR_DAYS.value * len(sections_list))

            # save the best chromosome as csv file in Schedules folder

            fileName =  'Schedule-' + str(randint(0, 10000)) + '.csv'
            file = open(fileName, 'w')
            file.write('section_id, instructor_id, day, time, room\n')
            for section in best_chromosome:
                file.write(str(section.id) + ',' + str(section.course_title) + ',' + str(section.instructor.name) + ',' + str(section.days_type) + ',' + str(section.start_time) + ',' + str(section.end_time) + '\n')
            file.close()

            schedule = Schedule.objects.create(fileName=fileName, fitness=best_fitness, conflict_fitness=best_conflict_fitness, fullLoad_fitness=best_fullLoad_fitness, fourDays_fitness=best_fourDays_fitness)
            schedule.save()


        return Response(status=status.HTTP_201_CREATED)

        