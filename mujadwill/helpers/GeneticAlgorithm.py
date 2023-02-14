import random

from .Fitness import FitnessEnum
from datetime import datetime



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

            instructorHours += sec.hours

        high = instructor.max_hours + 2
        low = instructor.max_hours - 2

        if (int(instructorHours) > high) or (int(instructorHours) < low):
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

        if not section.is_theory:

            # find the theory section from the instructor sections
            theory_section = section.theory_section
            is_assigned = False
            for sec in instructorSections:
                if sec == theory_section:
                    is_assigned = True
                    break

            if is_assigned:
                return FitnessEnum.LAB.value
            else:
                return 0
        
        return 0

    def calculatePreference(self, section, instructorSections):
        instructor = section.instructor
        instructorSections.append(section)
        instructorHours = 0
        
        preffernce = instructor.preference

        if preffernce is None:
            return FitnessEnum.PREFERENCE.value
        
        for sec in instructorSections:
            # check if sec time morning or night
            if sec.start_time < 12:
                time = 'morning'
            else:
                time = 'night'

            preffers_subjects = preffernce.preferred_subjects.split(',')

            isSubjectPreffered = False
            for subject in preffers_subjects:
                if subject == (sec.course_symbol + sec.course_id):
                    isSubjectPreffered = True
                    break
        
            
            if (preffernce.preferred_time == time) or (preffernce.preferred_days == sec.days_type) or isSubjectPreffered:
                return FitnessEnum.PREFERENCE.value
            else:
                return 0
            





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
        lab_fitness = 0
        preference_fitness = 0

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
            section_fitness += conflict
            conflict_fitness += conflict

            # 2. instructor has full load
            fullLoad = Helpers.calculateFullLoad(self, section, instructorSections)
            section_fitness += fullLoad
            fullLoad_fitness += fullLoad

            # 3. instructor has no more than 4 days
            fourDays = Helpers.calculateFourDays(self, section, instructorSections)
            section_fitness += fourDays
            fourDays_fitness += fourDays

            # 4. The instructor is assigned a class and with its lab.
            lab = Helpers.calculateLab(self, section, instructorSections)
            section_fitness += lab
            lab_fitness += lab

            # 5. Instructor has a preference
            preference = Helpers.calculatePreference(self, section, instructorSections)
            section_fitness += preference
            preference_fitness += preference


            fitness += section_fitness

            ranked_population.append((section, section_fitness))
            
            counter += 1
            
        return ranked_population, fitness, conflict_fitness, fullLoad_fitness, fourDays_fitness, lab_fitness, preference_fitness

    def crossover(self, ranked_population, instructors_list):
        
        leastRank = FitnessEnum.CONFLICT.value + FitnessEnum.FULL_LOAD.value + FitnessEnum.FOUR_DAYS.value + FitnessEnum.LAB.value + FitnessEnum.PREFERENCE.value

        # get the best of the population that has least rank
        best_population = [x for x in ranked_population if x[1] == leastRank]
        worst_population = [x for x in ranked_population if x[1] != leastRank]
        worst_population.sort(key=lambda x: x[1], reverse=True)

        worst_population_to_replace = worst_population[int(len(worst_population)/2):]




        # # sort the ranked population by the rank
        # ranked_population.sort(key=lambda x: x[1], reverse=True)

        # # get the best 50% of the population
        # best_population = ranked_population[:int(len(ranked_population)/2)]

        # # get the worst 50% of the population
        # worst_population = ranked_population[int(len(ranked_population)/2):]

        # loop on worst population and swap instructors randmoly
        for section in worst_population_to_replace:

            # select random instructor
            random_instructor = random.choice(instructors_list)
            section[0].instructor = random_instructor

        worst_population = worst_population_to_replace + worst_population[:int(len(worst_population)/2)]
        # remove the section rank from the list
        best_population = [x[0] for x in best_population]
        worst_population = [x[0] for x in worst_population]
        
        # add the best population to the worst population
        new_population = best_population + worst_population


        return new_population

