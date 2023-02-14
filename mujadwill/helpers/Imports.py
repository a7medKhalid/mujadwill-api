import pandas as pd
from ..models import Section, Instructor
from datetime import datetime
import random
import string

from math import ceil

def importSectionsFunction(file):
     # import arabic xlsx file
    data = pd.read_excel(file)

    # loop through each row
    for index, row in data.iterrows():
        if row['المقرر'] != 'CCSW':
            continue

        # get the days type
        # concatenate the days type

        days_type = str(row['الاحد']) + str(row['الاثنين']) + str(row['الثلاثاء']) + str(row['الأربعاء']) + str(row['الخميس'])
        # remove n letter from the days type
        days_type = days_type.replace('nan', '')
        
        # check if the section is theory or lab
        if row['رمز الجدولة'] == 'L':
            is_theory = True
        else:
            is_theory = False

        # add section to database

        try:
            shu3bah = row['الشعبة']
        except:
            shu3bah = None

        # if lab hours 1 else get real hours
        if is_theory:
            # count section hours
            start_time = row['البداية']
            end_time = row['النهاية']

            startTime = datetime.strptime(str(int(start_time)), '%H%M').time()
            endTime = datetime.strptime(str(int(end_time)), '%H%M').time() 
            diff = datetime.combine(datetime.min, endTime) - datetime.combine(datetime.min, startTime)
            diff = float((diff.total_seconds())) / 3600

            days_count = len(days_type)
            realHours = diff * days_count
            realHours = ceil(realHours)


        else:
            realHours = 1
        
        # create section object
        section = Section(row['م'], row['المقرر'], row['رقمه'], shu3bah, is_theory, row['عنوان المقرر'], row['البداية'], row['النهاية'], days_type, hours=realHours)
        
        # check if the section is theory or lab
        if not section.is_theory:
            # get pervious section
            theory_section = Section.objects.latest('id')
            # set the theory section
            section.theory_section = theory_section
    
        section.save()

def importInstructorsFunction(file):
    # import arabic xlsx file
    data = pd.read_excel(file)

    # loop through each row
    for index, row in data.iterrows():
        random_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        # add instructor to database
        instructor = Instructor(name=row['اسم المدرس'], max_hours=row['الحد الأقصى لعدد الساعات'], university_id=row['الرقم الجامعي'], secret_token=random_token)
        instructor.save()
