import json
from back_end import selecting_class

#grades and gpa main menu
def calculate_menu():
    while True:
        print('\n------------------\nGRADES AND GPA\n-------------------\n1. View grades \n2. Add/edit grades\n3. GPA Calculator\n4. Add your GPA\n0. EXIT')
        calc_menu = input('\nEnter choice: ').strip().lower()

        # view grades
        if calc_menu == '1':

            with open('class_grades.json') as f:
                    all_grades = json.load(f)
            print('\nCurrent Averages for Your Classes\n---------------')
            for key,value in all_grades.items():
                grade = str(value)
                print(key, ': ', grade,'%')
            print('\nNOTE:\nGrades will not be calculated if the grading scale is incomplete. \n- To add full grading scale, go to: -> 2. Add/edit grades -> 1. Add new grades\n')
            while True:
                choice = input('\nView gradebook for a class (y/n)?: ').strip().lower()
                if choice == 'y' or choice == 'yes': #view indiv class grade
                    class_name = selecting_class()
                    if class_name == 'back':
                        break
                    with open('gradebook.json') as f:
                        grades = json.load(f)
                    if class_name not in grades:
                        print('\nERROR. No grades entered for',class_name,'. Please go to --> 2. Add/edit grades --> 1. Add new grades\n')
                        grades[class_name] = {}
                        with open('gradebook.json','w') as f:
                            json.dump(grades, f,indent=4)
                        break
                    gradebook = grades[class_name]
                    print('\nGrade Book for ', class_name,'\n---------------')
                    for key, value in gradebook.items():
                        print(key, ': ', value)
                    again = input('\nView another class (y/n)? ')
                    if again == 'y' or again == 'yes':
                        continue
                    elif again == 'n' or again == 'no':
                        break
                    else:
                        print('\nPlease enter yes or no')
                        continue
                elif choice =='n' or choice == 'no':
                    break
                else:
                    print('\nERROR. Please enter yes or no')
                    continue

        #add edit grades
        elif calc_menu =='2':
            class_name = selecting_class()
            while True:
                if class_name == 'back':
                    break

                print('\n---------\nGrade Options\n----------')
                edit = input('1. Add new grades\n2. Edit existing grade\n0. Back\nEnter choice: ').strip()

                if edit == '1': #add new grades
                    entering_grades(class_name)
                    break
                elif edit == '2': #edit existing grade
                    editing_grades(class_name)
                    break
                elif edit == '0':
                    print('Going back....')
                    break
        elif calc_menu == '3': #gpa calc
            calc_gpa()
            break
        elif calc_menu == '4': #adding gpa
            gpa_file = 'gpa.json'
            while True:
                gpa_data = creating_gpa()
                print('\nSaving your GPA...')
                save_gpa(gpa_file, gpa_data)
                print('\nGPA saved.')
                break
        elif calc_menu == '0':
            break
        else:
            print('\nERROR. Please enter a valid choice.')

#add new grades
def entering_grades(class_name):
    # opening grading scale
    try:
        with open('classes.json') as f:
            classes = json.load(f)
    except FileNotFoundError:
        classes={}

    #opening gradebook
    try:
        with open('gradebook.json') as f:
            gradebook = json.load(f)
    except FileNotFoundError:
        gradebook ={}

    #opening class averages
    try:
        with open('class_grades.json') as f:
            class_grades = json.load(f)
    except FileNotFoundError:
        class_grades={}

    #adding new class to grade book
    if class_name not in gradebook:
        gradebook[class_name] = {}

    assignments = classes[class_name]['Assignments']

    while True:
        #if no grading scaling
        if len(assignments) == 0:
            print('\nNo grading scale has been added for', class_name,'. Would you like to add a section?')
            add_section = input('(y/n): ').lower().strip()
            while True:
                if add_section == 'y' or add_section == 'yes':
                    assignment_name = input('\nEnter the name of the section: ').strip().title()
                    while True:
                        try:
                            weight = float(input('Enter the weight (.15, .20,etc): '))
                            break
                        except ValueError:
                            print('\nERROR. Please enter a valid weight.')

                    assignments[assignment_name] = weight
                    classes[class_name]['Assignments'] = assignments

                    with open('classes.json', 'w') as f: #add grading scale to classes.json
                        json.dump(classes, f, indent=4)

                    another = input('\nWould you like to add another section? (y/n): ').lower().strip()
                    if another == 'y' or another == 'yes':
                        continue
                    elif another == 'n' or another == 'no':
                        break
                    else:
                        print('\nERROR. Please enter yes or no.')
                        continue
                elif add_section == 'n' or add_section == 'no':
                    return
                else:
                    print('\nERROR. Please enter yes or no.')
                    continue
        print('\n--------------\nSections For', class_name, '\n-------------')

        # display sections to add to
        for name in assignments:
            print('-', name)
        while True:
            print('\nHow many sections?')
            all_or_one = input('Enter multiple, one, or exit: ').lower().strip()

            #this is broken
            if all_or_one == 'multiple':
                print('\n-------PLEASE NOTE--------')
                print('- Enter scores as a number (ex. 88, 100).')
                print('- Enter \'done\' to finish.')
                for name in assignments:
                    if name not in gradebook[class_name]:#create new list of grades for that section
                        gradebook[class_name][name] = []
                    print('Entering grades for', name)
                    while True:
                        score = input('Score: ').strip().lower()

                        if score=='done':
                            print('\nSaving grades....')
                            with open('gradebook.json', 'w') as f:
                                json.dump(gradebook, f, indent=4)
                            print('\nGrades saved.')
                            total = sum(assignments.values())
                            if total >= 1:
                                class_grades[class_name] = calc_grade_percentage(class_name)
                                save_class_grade('class_grades.json', class_grades)
                            return
                        try:
                            score = float(score)
                            gradebook[class_name][name].append(float(score))
                        except ValueError:
                            print('Please enter a valid score or \'done\'.')
                            continue
            elif all_or_one == 'one' or all_or_one == '1':
                while True:
                    assignment_name = input('\nEnter the name of the section: ').strip().title()
                    if assignment_name =='Exit':
                        return

                    if assignment_name not in assignments:
                        print('\nAdd',assignment_name, 'to the grade book?\nEnter \'n\' if you would like to retype or \'exit\' to cancel.')
                        add_new_section = input('Enter (y/n): ').strip().lower()
                        if add_new_section == 'y' or add_new_section == 'yes':
                            while True:
                                try:
                                    weight = float(input('Enter the weight (.15, .20,etc): '))
                                    break
                                except ValueError:
                                    print('ERROR. Please enter a valid weight.')
                            assignments[assignment_name] = weight
                            classes[class_name]['Assignments'] = assignments
                            with open('classes.json','w') as f:
                                 json.dump(classes, f, indent=4)
                            break

                        elif add_new_section == 'n' or add_new_section == 'no':
                            continue
                        elif add_new_section == 'exit':
                            return
                        else:
                            print('\nERROR. Please enter yes or no.')
                            continue
                    if assignment_name not in gradebook[class_name]:
                        gradebook[class_name][assignment_name] = []
                    print('\nEntering grades for', assignment_name,'...')
                    print('\n-------PLEASE NOTE--------')
                    print('- Enter scores as a number (ex. 88, 100).')
                    print('- Enter \'done\' to finish.')
                    while True:
                        score = input('Score: ').strip().lower()
                        if score=='done':
                            print('\nSaving grades....')

                            with open('gradebook.json', 'w') as f:
                                json.dump(gradebook, f, indent=4)
                            print('\nGrades saved.')
                            total = sum(assignments.values())
                            if total >= 1:
                                class_grades[class_name] = calc_grade_percentage(class_name)
                                save_class_grade('class_grades.json', class_grades)
                            return
                        try:
                            score = float(score)
                            gradebook[class_name][assignment_name].append(float(score))
                        except ValueError:
                            print('\nERROR. Please enter a valid score or \'done\'.')
                            continue
                        #brain is fried
            elif all_or_one == 'exit':
                return
            else:
                print('\nERROR. Enter a valid input.')

#editing/fixing old grades
def editing_grades(class_name):
    try:
        with open('gradebook.json') as f:
            gradebook = json.load(f)
    except FileNotFoundError:
        gradebook ={}

    try:
        with open('classes.json') as f:
            classes = json.load(f)
    except FileNotFoundError:
        classes = {}

    try:
        with open('class_grades.json') as f:
            class_grades = json.load(f)
    except FileNotFoundError:
        class_grades = {}


    assignments = classes[class_name]['Assignments']

    while True:
        assignment_list = {}
        count = 1
        if len(assignments)==0 :
            print('\nNo grading scale found for',class_name,'. \nPlease go back and go to: -> \'2. Add/edit grades\' -> Select',class_name,'-> \'1. Add new grades\' to add grading scale. ')
            break
        if class_name not in gradebook or len(gradebook[class_name])==0:
            print('\nNo grades were added for',class_name,'. \nPlease go back and go to: -> \'2. Add/edit grades\' -> Select',class_name,'-> \'1. Add new grades\' to add grades. ')
            break


        print('\n------------\nASSIGNMENTS\n------------')

        for assignment,grades in gradebook[class_name].items():
            print(count, '.', assignment,': ',grades)
            assignment_list[count] = assignment
            count += 1
        print('0. Back')

        while True:
            try:
                selected = int(input('\nEnter choice: '))
                break
            except ValueError:
                print('ERROR. Please enter a number choice.')

        if selected ==0:
            print('\nExiting...')
            break
        if selected not in assignment_list:
            print('\nERROR. Please enter a valid choice.')
            continue

        if selected in assignment_list:
            selected_assignment = assignment_list[selected]
            assignment = gradebook[class_name][selected_assignment]
            if len(assignment)==1:
                while True:
                    try:
                        updated_grade = float(input('\nEnter the updated score: '))
                        gradebook[class_name][selected_assignment]=[updated_grade]
                        with open('gradebook.json', 'w') as f:
                            json.dump(gradebook, f, indent=4)
                        print('\nGrade updated.')
                        total = sum(assignments.values())
                        if total >= 1:
                            class_grades[class_name] = calc_grade_percentage(class_name)
                            save_class_grade('class_grades.json', class_grades)

                        break
                    except ValueError:
                        print('\nPlease enter a valid score.')
                        continue
            else:
                number = 1
                print('\nCurrent scores for ',selected_assignment,': ')
                for score in assignment:
                    print(number, '.',score)
                    number +=1
                while True:
                    try:
                        index = int(input('\nEnter the number of the score to update: '))
                        break
                    except ValueError:
                        print('\nERROR. Please enter a valid number.')
                        continue

                while True:
                    try:
                        updated_grade = float(input('Updated score: '))
                        assignment[index-1] = updated_grade
                        with open('gradebook.json', 'w') as f:
                            json.dump(gradebook, f, indent=4)
                        print('\nUpdates saved.')
                        total = sum(assignments.values())
                        if total >= 1:
                            class_grades[class_name] = calc_grade_percentage(class_name)
                            save_class_grade('class_grades.json', class_grades)

                        break
                    except ValueError:
                        print('Please enter a valid score.')
                        continue

#saving grades
def save_class_grade(filename, grade):
    filename = 'class_grades.json'
    with open(filename,'w') as f:
        json.dump(grade,f,indent=4)

#viewing grades
def view_grades(class_name):
    with open('gradebook.json','r') as f:
        gradebook = json.load(f)
    grades = gradebook[class_name]
    print('\nCurrent grades for ', class_name)
    for key, value in grades.items():
        print(key, '-', value)

#calculating grade
def calc_grade_percentage(class_name):
    #open grading section
    with open('classes.json') as f:
        classes=json.load(f)
    #open grades
    with open('gradebook.json') as f:
        gradebook = json.load(f)

    #getting weight of section
    weights = classes[class_name]['Assignments']

    #getting grades of section
    grades = gradebook[class_name]

    total_weight = 0
    final_grade = 0
    total_weight = 0
    final_grade = 0

    for section, weight in weights.items():
        if section in grades and len(grades[section]) > 0:
            avg = sum(grades[section]) / len(grades[section])
            final_grade += avg * weight
            total_weight += weight

    if total_weight > 0:
        final_grade = final_grade / total_weight

    grade = round(final_grade, 2)

    print('\nCurrent grade for ', class_name, ': ', grade, '%')


    return grade

#adding gpa info
def creating_gpa():
    current_gpa = float(input('\nWhat is your current gpa?\n'))
    hours = int(input('\nHow many hours have you already completed? \n'))
    gpa_data = {
        'current_gpa':current_gpa,
        'hours':hours
    }
    return gpa_data

#save gpa info
def save_gpa(gpa_file,gpa_data):
    with open(gpa_file,'w') as f:
        json.dump(gpa_data, f, indent=4)

#calculate gpa
def calc_gpa():
    try:
        with open('gpa.json','r') as f:
            gpa_data=json.load(f)
    except Exception as e:
        print('\nNo GPA data found. Please go to: ---> \"4. Add your GPA\".')
        return
    current = gpa_data['current_gpa']
    hours = gpa_data['hours']
    current_points = current * hours
    grade_scale = {
        'A+': 4.3, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1, 'F': 0
    }
    while True:
        try:
            class_num = int(input('\nHow many class are you calculating for? \n'))
        except ValueError:
            print('\nPlease enter a number.\n')
            continue
        newPoints = 0
        newHours = 0
        for x in range(0, class_num):
            while True:
                try:
                    class_credits = int(input('\nCredits for class ' + str(x+1) + ':\n'))
                    break
                except ValueError:
                    print('\nPlease enter a number.\n')
            while True:
                grade = input('\nEnter letter grade (A+, A-, A, etc): ').upper().strip()

                if grade in grade_scale:
                    break
                print('Invalid grade. Please re-enter.')
            points = class_credits * grade_scale[grade]
            newHours += class_credits
            newPoints += points
        total_hours = hours + newHours
        total_points = current_points + newPoints
        GPA = total_points / total_hours
        print('\nyour new gpa will be', round(GPA, 2),'. \n')
        break




