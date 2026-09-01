import json
from create_save_classes import create_class
from create_save_classes import save_class
from create_save_classes import edit_class
from create_sched import school_sched
# from create_sched import save_schedule
from create_sched import no_school
from ai_settings import gem_greeting
from ai_settings import Bob
from ai_settings import gem_adios

#bob settings
def AI_QuickSearch_menu(): 
    try:
        print(gem_greeting())
    except Exception as e:
        print('The AI feature isn\'t working right now. Please try again later.')
        print('ERROR: ',e)
        return
    print('\nEnter your question or type \'quit\' to exit: ')
    while True:
        student_q = input('> ').lower().strip()
        if student_q == 'quit' or student_q=='exit' or student_q=='bye' or student_q=='goodbye':
            try:
                print(gem_adios(student_q))
            except Exception as e:
                print('ERROR: ',e)
            break
        try:
            print(Bob(student_q))
        except Exception as e:
            print('Sorry, that question couldn\'t be answered right now. Please try again.')
            print('ERROR: ',e)

#manually view info
def manual_menu():
    print('\nWelcome to the Manual View. Here, you can manually view all your information.')
    while True:
        main = input('\n--------------\nManual View\n--------------\n1. View all schedules\n2. View class syllabus information\n0. Back\nEnter choice: ')
        if main =='1':
            view_school_info()
        elif main =='2':
            chosen_class = selecting_class()
            if chosen_class == 'back':
                break
            else:
                class_menu_options(chosen_class)
        elif main =='0':
            break
        else:
            print('Invalid choice')

#view school menu
def view_school_info():
    while True:

        try:
            with open('school_sched.json') as f:
                schedule_data = json.load(f)
        except FileNotFoundError:
            schedule_data = {}

        sched_choice = input('\n--------------\nSchool Information Menu\n--------------\n1. View yearly schedule\n2. View semester schedule\n3. View schedule of classes\n0. EXIT\nEnter your choice: ').strip()

        # view yearly
        if sched_choice == '1':
            for year,semesters in schedule_data.items():
                print('----------\n',year,'Schedule\n-----------')
                for semester,schedule in semesters.items():
                    print('\n',semester,'\n----------')
                    for key,value in schedule.items():
                        print(key, ': ', value, '\n')

        #view semester
        elif sched_choice == '2':
            while True:
                count = 1
                year_list ={}
                print('\n--------\nYear List\n---------')
                for year in schedule_data:
                    print(count, '.', year)
                    year_list[count] = year
                    count += 1
                print('0. EXIT')
                try:
                    year_choice = int(input('\nPlease type the number of the year:'))
                except ValueError:
                    print('\nERROR. Please enter a number.\n')
                    continue
                if year_choice ==0:
                    break
                if year_choice not in year_list:
                    print('\nERROR. Please enter a valid year.\n')
                    continue
                chosen_year = year_list[year_choice]

                count = 1
                sem_list = {}
                print('\n--------\nSemester List\n---------')
                for semester in schedule_data[chosen_year]:
                    print(count, '.', semester)
                    sem_list[count] = semester
                    count += 1
                print('0. BACK')
                try:
                    sem_choice = int(input('\nPlease type the number of the semester:'))
                except ValueError:
                    print('\nERROR. Please enter a number.\n')
                    continue
                if sem_choice == 0:
                    continue
                if sem_choice not in sem_list:
                    print('\nERROR. Please enter a valid semester.\n')
                    continue
                chosen_sem = sem_list[sem_choice]
                print('---------------')
                print(chosen_year, chosen_sem, 'Semester Schedule')
                print('---------------')
                for key,value in schedule_data[chosen_year][chosen_sem].items():
                    print(key, ': ', value, '\n')
                break

        # view class schedule
        elif sched_choice =='3':
            print('\n-----------------\nClass Schedule\n-----------------')

            try:
                with open('classes.json') as f:
                    classes = json.load(f)
            except FileNotFoundError:
                classes = {}

            for class_name in classes:
                print('\n',class_name,'\n------------')

                time = classes[class_name]['Class Time']
                location = classes[class_name]['Class Location']
                for key, value in time.items():
                    print(key, ': ', value, '\n')
                for key,value in location.items():
                    print(key, ': ', value, '\n')

        elif sched_choice == '0': #exit
            break

#settings menu
def settings():
    filename = 'classes.json'
    while True:
        settings_choice = input('\n--------------\nADD/EDIT INFORMATION\n----------------\n1. Add class\n2. Edit class\n3. Create yearly schedule\n0. Back\nEnter choice: ').strip()
        if settings_choice =='1': #add class
            try:
                with open(filename) as f:
                    classes=json.load(f)
            except FileNotFoundError:
                classes = {}
            while True:
                create = input('\nCreate class? (y/n): ').strip()
                if create == 'n' or create == 'no':
                    break
                elif create == 'y' or create == 'yes':
                    classes = create_class(classes)
                    print('\nSaving class...')
                    save_class(classes, filename)
                    print('\nClass saved.')
                else:
                    print('ERROR. Please enter yes or no')
        elif settings_choice =='2':#edit class
            with open(filename,'r') as f:
                classes = json.load(f)

            edit_class(classes,filename)
        elif settings_choice =='3':#add schedule
            year = input('Enter the year: ')
            semester = input('Enter school semester (spring/fall/summer): ').strip().title()
            while True:
                create_sched = input('\nCreate school semester schedule? (y/n): ')
                if create_sched == 'y' or create_sched == 'yes':
                    school_sched(year, semester)
                    try:
                        with open('school_sched.json') as f:
                            schedule_data = json.load(f)
                    except Exception as e:
                        schedule_data= {}
                    schedule = schedule_data[year][semester]
                    print('\nHere is your schedule\n---------------')
                    for key,value in schedule.items():
                        print(key, ': ', value,'\n')
                if create_sched == 'n' or create_sched == 'no':
                    add_breaks = input('Add holidays and/or breaks? (y/n): ').strip().lower()
                    if add_breaks == 'y' or add_breaks == 'yes':
                        no_school(year,semester)
                        break
                    elif add_breaks == 'n' or add_breaks == 'no':
                        break
                    else:
                        print('ERROR.Please enter yes or no. ')
                else:
                    print('ERROR. Please enter yes or no. ')
        elif settings_choice== '0':
            break
        else:
            print('ERROR. Please enter a valid choice.')

#choosing class
def selecting_class():
    print('\n--------------\nCLASSES\n--------------\n')

    #loading classes
    try:
        with open('classes.json') as f:
            classes = json.load(f)
    except FileNotFoundError:
        classes = {}
    count = 1
    class_list = {}
    for class_name in classes:
        print(count, '.',class_name)
        class_list[count] = class_name
        count += 1
    print('0 . Back')
    while True:
        choose = input('\nSelect class number: ')
        try:
            choose = int(choose)
            if choose in class_list:
                return class_list[choose]
            elif choose == 0:
                return 'back'
            else:
                print('\nERROR. Please enter a valid choice.')
        except ValueError:
            print('\nERROR. Please enter a number choice.')

#class menu options
def class_menu_options(chosen_class):
    try:
        with open('classes.json') as f:
            classes = json.load(f)
    except FileNotFoundError:
        classes = {}

    while True:
        print('\n1. View contacts\n2. View schedule\n3. View location\n4. View policies\n5. View class materials\n6. View grading scale\n0. Exit')
        option = input('\nEnter your choice: ')
        class_time = classes[chosen_class]['Class Time']
        contacts = classes[chosen_class]['Contacts']
        location = classes[chosen_class]['Class Location']
        policies = classes[chosen_class]['Policies']
        work_policy = classes[chosen_class]['Late Assignment Policy']
        materials = classes[chosen_class]['Course Materials']
        grading_scale = classes[chosen_class]['Assignments']

        if option == '1':
            print('\n-------------\nCONTACTS LIST\n-------------')
            for contact, info in contacts.items():
                print('- ',contact,': ', info)
        elif option == '2':
            print('\n-------------\nCLASS DAY AND TIME\n-------------')
            for day, time in class_time.items():
                print('- ',day,': ', time)
        elif option == '3':
            print('\n----------------\nCLASS LOCATION\n----------------')
            for place, room in location.items():
                print('- ',place,': ', room)
        elif option == '4':
            print('\n-------------\nPOLICIES\n-------------')
            print('- Late Assignment Policy: ', work_policy)
            for key, value in policies.items():
                print('-',key,': ', value)
        elif option == '5':
            print('\n-------------\nCLASS MATERIALS\n-------------')
            print('- ', materials)
        elif option == '6':
            print('\n-------------\nGRADING SCALE\n-------------')
            while True:
                if len(grading_scale) == 0:
                    print('No grading scale added. Please add in settings.')
                    break
                for name, weight in grading_scale.items():
                    print('- ', name, ': ', weight)
                break
        elif option == '0':
            break
        else:
            print('ERROR: Please enter a valid choice.')

def deleting_class():
    try:
        with open('classes.json') as f:
            classes = json.load(f)
    except Exception as e:
        print(e)
        classes={}
    try:
        with open('class_grades.json') as f:
            averages = json.load(f)
    except Exception as e:
        print(e)
        averages = {}
    try:
        with open('gradebook.json') as f:
            gradebook = json.load(f)
    except Exception as e:
        print(e)
        gradebook = {}


    print('\nPlease choose a class to delete.')
    class_name = selecting_class()
    if class_name in classes:
        confirm = input('Are you sure you want to delete '+ class_name+'?\nThis cannot be undone.\n(y/n): ').lower().strip()
        if confirm == 'y' or confirm == 'yes':
            del classes[class_name]
            averages.pop(class_name, None)
            gradebook.pop(class_name, None)
            with open('classes.json', 'w') as f:
                json.dump(classes, f,indent=4)
            with open('class_grades.json', 'w') as f:
                json.dump(averages, f,indent=4)
            with open('gradebook.json', 'w') as f:
                json.dump(gradebook, f,indent=4)
            print('\nClass deleted.')
            return
        elif confirm == 'n' or confirm == 'no':
            return
        else:
            print('ERROR. Please enter yes or no.')

def deleting_sem_sched():
    try:
        with open('school_sched.json') as f:
            schedule = json.load(f)
    except Exception as e:
        print(e)
        schedule = {}

    if len(schedule) == 0:
        print('\nNo schedules found.')
        return

    count = 1
    year_list = {}
    print('\n--------\nYear List\n---------')
    for year in schedule:
        print(count, '.', year)
        year_list[count] = year
        count += 1
    print('0. Back')
    try:
        year_choice = int(input('\nPlease type the number of the year: '))
    except ValueError:
        print('\nERROR. Please enter a number.\n')
        return
    if year_choice == 0:
        return
    if year_choice not in year_list:
        print('\nERROR. Please enter a valid year.\n')
        return
    chosen_year = year_list[year_choice]

    count = 1
    sem_list = {}
    print('\n--------\nSemester List\n---------')
    for semester in schedule[chosen_year]:
        print(count, '.', semester)
        sem_list[count] = semester
        count += 1
    print('0. Back')
    try:
        sem_choice = int(input('\nPlease type the number of the semester: '))
    except ValueError:
        print('\nERROR. Please enter a number.\n')
        return
    if sem_choice == 0:
        return
    if sem_choice not in sem_list:
        print('\nERROR. Please enter a valid semester.\n')
        return
    chosen_sem = sem_list[sem_choice]

    confirm = input('Are you sure you want to delete '+chosen_year+' '+chosen_sem+'?\nThis cannot be undone.\n(y/n): ').lower().strip()
    if confirm == 'y' or confirm == 'yes':
        del schedule[chosen_year][chosen_sem]
        if len(schedule[chosen_year]) == 0:
            del schedule[chosen_year]
        with open('school_sched.json', 'w') as f:
            json.dump(schedule, f, indent=4)
        print('\nSchedule deleted.')
    elif confirm == 'n' or confirm == 'no':
        return
    else:
        print('ERROR. Please enter yes or no.')

