import json

#add yearly schedule
# def create_schedule(schedule_data):
#     semester = input('Enter school semester (spring/fall/summer): ').strip().capitalize()
#     print('Please enter all dates in this format: JAN 01 - JAN 02')
#     sched_classes_avail = input('Enter date for schedule of classes available: ').upper().strip()
#     registration = input('Enter registration period: ').upper().strip()
#     class_start = input('Enter classes start date:  ').upper().strip()
#     late_reg = input('Enter late registration period: ').upper().strip()
#     midpoint = input('Enter midpoint date: ').upper().strip()
#     end_classes = input('Enter end of classes date: ').upper().strip()
#     exam = input('Enter exam period: ').upper().strip()
#     final_grades = input('Enter date of final grades available: ').upper().strip()
#     schedule_data[semester] = {
#         'schedule of classes available': sched_classes_avail,
#         'registration period': registration,
#         'classes begin': class_start,
#         'late registration period': late_reg,
#         'midpoint': midpoint,
#         'end of classes': end_classes,
#         'exam period': exam,
#         'final grades available': final_grades
#     }
#     return schedule_data

#save
# def save_schedule(schedule_data,schedule_file):
#     with open(schedule_file,'w') as f:
#         json.dump(schedule_data,f,indent=4)

#add holidays and breaks
# def add_holidays_and_breaks(year,semester):
#     try:
#         with open('no_school.json') as f:
#             no_school = json.load(f)
#     except Exception as e:
#         no_school = {}
#     print('Please enter all dates in this format: JAN 1 - JAN 2')
#     holidays = {}
#     breaks = {}
#     while True:
#         holiday_name = input('Enter holiday name: ' ).strip().title()
#         holi_date = input('Enter holiday date: ').upper()
#         holidays[holiday_name] = holi_date
#         add_another = input('\nAdd another holiday? (y/n) ').strip().lower()
#         if add_another == 'y' or add_another == 'yes':
#             continue
#         elif add_another == 'n' or add_another == 'no':
#             break
#         else:
#             print('ERROR. Please enter yes or no.')
#     while True:
#         breaks_question = input('Do you want to add breaks(y/n)? ').strip().lower()
#         if breaks_question == 'y' or breaks_question == 'yes':
#             break_name = input('Enter break name: ').title()
#             break_date = input('Enter break date: ').upper()
#             breaks[break_name] = break_date
#         elif breaks_question == 'n' or breaks_question == 'no':
#             break
#         else:
#             print('ERROR. Please enter yes or no.')
#
#     no_school[year][semester] = {
#     'holidays':holidays,
#     'breaks':breaks
#     }
#
#     try:
#         with open('no_school.json','w') as f:
#             json.dump(no_school,f,indent=4)
#     except Exception as e:
#         #print(e)
#         no_school ={}
# #load schedule
def load_schedule(filename='2026.json'):
    try:
        with open(filename,'r') as f:
            schedule= json.load(f)
            return schedule
    except FileNotFoundError:
        return {}


def school_sched(year,semester):
    try:
        with open('school_sched.json') as f:
            school_schedule= json.load(f)
    except Exception as e:
        school_schedule = {}

    print('\nPlease enter all dates in this format: JAN 01 - JAN 02\n')
    sched_classes_avail = input('Enter date for schedule of classes available: ').upper().strip()
    registration = input('Enter registration period: ').upper().strip()
    class_start = input('Enter classes start date:  ').upper().strip()
    late_reg = input('Enter late registration period: ').upper().strip()
    midpoint = input('Enter midpoint date: ').upper().strip()
    end_classes = input('Enter end of classes date: ').upper().strip()
    exam = input('Enter exam period: ').upper().strip()
    final_grades = input('Enter date of final grades available: ').upper().strip()
    if year not in school_schedule:
        school_schedule[year] = {}

    school_schedule[year][semester] =     {
        'schedule of classes available': sched_classes_avail,
        'registration period': registration,
        'classes begin': class_start,
        'late registration period': late_reg,
        'midpoint': midpoint,
        'end of classes': end_classes,
        'exam period': exam,
        'final grades available': final_grades
                                  }

    try:
        with open('school_sched.json','w') as f:
            json.dump(school_schedule,f,indent=4)
    except Exception as e:
        school_schedule ={}

def no_school(year, semester):
    try:
        with open('no_school.json') as f:
            no_school = json.load(f)
    except Exception as e:
        no_school = {}

    holidays = {}
    breaks ={}
    print('Please enter all dates in this format: JAN 1 - JAN 2')
    add_holiday = input('Add a holiday? (y/n) ').strip().lower()
    while add_holiday == 'y' or add_holiday == 'yes':
        holiday_name = input('Enter holiday name: ' ).strip().title()
        holi_date = input('Enter holiday date: ' ).upper()
        holidays[holiday_name] = holi_date

        add_holiday = input('Add another holiday? (y/n) ').strip().lower()

    add_breaks = input('Add a breaks? (y/n) ').strip().lower()
    while add_breaks == 'y' or add_breaks == 'yes':
        breaks_name = input('Enter break name: ' ).strip().title()
        breaks_date = input('Enter break date: ' ).upper()
        breaks[breaks_name] = breaks_date

        add_breaks = input('Add another break? (y/n) ').strip().lower()

    if year not in no_school:
        no_school[year] = {}
    no_school[year][semester] = {
        'holidays':holidays,
        'breaks':breaks
    }
    try:
        with open('no_school.json','w') as f:
            json.dump(no_school,f,indent=4)
    except Exception as e:
        #print(e)
        no_school ={}