import pandas as pd
from ..models import Section, Instructor

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

        
        # create section object
        section = Section(row['م'], row['المقرر'], row['رقمه'], row['الشعبة'], is_theory, row['عنوان المقرر'], row['البداية'], row['النهاية'], days_type)
        
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
        
        # add instructor to database
        instructor = Instructor(name=row['اسم المدرس'], max_hours=row['الحد الأقصى لعدد الساعات'], university_id=row['الرقم الجامعي'])
        instructor.save()
