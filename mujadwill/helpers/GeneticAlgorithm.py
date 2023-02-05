import random

from .Fitness import FitnessEnum


class Helpers:
    def calculateConflict(self, section, instructorSections):
        conflict = False
        for sec in instructorSections:
            conflict = False
            days_type = sec.days_type
            startTime = sec.start_time
            endTime = sec.end_time
            if section.days_type == days_type and section.start_time == startTime and section.end_time == endTime:
                conflict = True
                break
                
        if conflict:
            return 0
        else:
            return FitnessEnum.CONFLICT.value

    def calculateFullLoad(self, section, instructorSections):
        instructorSections.append(section)
        instructor = section.instructor
        instructorHours = 0
        for sec in instructorSections:
            instructorHours += sec.end_time - sec.start_time

        if instructorHours > instructor.max_hours:
            return 0
        else:
            return FitnessEnum.FULL_LOAD.value
    
    def calculateFourDays(self, section, instructorSections):
        instructorSections.append(section)
        instructorDays = []
        for sec in instructorSections:
            days_type = sec.days_type
            # remove spaces from the days type
            days_type = days_type.replace(' ', '')
            for day in days_type:
                if day not in instructorDays:
                    instructorDays.append(day)

        if len(instructorDays) > 4:
            return 0
        else:
            return FitnessEnum.FOUR_DAYS.value
    
    def calculateLab(self, section, instructorSections):
        instructorSections.append(section)
        instructor = section.instructor
        instructorHours = 0


class GeneticAlgorithmClass:
    
    def generatePopulation(self, sections_list, instructors_list):
        # create list of sections with instructors
        population = []

        for s in sections_list:
            # select random instructor
            random_instructor = random.choice(instructors_list)
            s.instructor = random_instructor
            
            population.append(s)

        return population

    def calculateFitness(self,population):

        
        fitness = 0
        ranked_population = []
        conflict_fitness = 0
        fullLoad_fitness = 0
        fourDays_fitness = 0

        counter = 0

        # remove last item from the list
        
        for section in population:

            if section == None:
                break
            
            instructor = section.instructor
            
            # without the current section
            instructorSections = [x for x in population if x.instructor == instructor and x != section]

            section_fitness = 0

            # constraints
            # 1. instructor has no conflicts
            conflict = Helpers.calculateConflict(self, section, instructorSections)
            fitness += conflict
            section_fitness += conflict
            conflict_fitness += conflict

            # 2. instructor has full load
            fullLoad = Helpers.calculateFullLoad(self, section, instructorSections)
            fitness += fullLoad
            section_fitness += fullLoad
            fullLoad_fitness += fullLoad

            # 3. instructor has no more than 4 days
            fourDays = Helpers.calculateFourDays(self, section, instructorSections)
            fitness += fourDays
            section_fitness += fourDays
            fourDays_fitness += fourDays

            # 4. The instructor is assigned a class and with its lab.

            # 5. The instructor has his prefrences



            ranked_population.append((section, section_fitness))
            
            counter += 1
            
        return ranked_population, fitness, conflict_fitness, fullLoad_fitness, fourDays_fitness

    def crossover(self, ranked_population, instructors_list):

        # sort the ranked population by the rank
        ranked_population.sort(key=lambda x: x[1], reverse=True)

        # get the best 50% of the population
        best_population = ranked_population[:int(len(ranked_population)/2)]

        # get the worst 50% of the population
        worst_population = ranked_population[int(len(ranked_population)/2):]

        # loop on worst population and swap instructors randmoly
        for section in worst_population:
            # select random instructor
            random_instructor = random.choice(instructors_list)
            section[0].instructor = random_instructor

        # remove the section rank from the list
        best_population = [x[0] for x in best_population]
        worst_population = [x[0] for x in worst_population]
        
        # add the best population to the worst population
        new_population = best_population + worst_population

        return new_population

