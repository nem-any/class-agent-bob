import json


#adding classes
def create_class(classes):
    #getting class info
    class_name = input('Enter class name (ex. CIS 3260 - INTRO TO PROGRAMMING): ').upper().strip()
    professor_name = input('Enter your professor\'s name: ').strip().title()
    prof_email = input('Enter your professor\'s email: ').strip().lower()
    ta = input('Enter your TA\'s name:' ).title().strip()
    ta_email = input('Enter your TA\'s email: ').strip().lower()
    materials = input('Enter the course texts and materials or \'none\': ').strip()
    attendance = input('Enter the attendance policy: ').strip()
    #checking for free drops
    while True:
        attendance_free_drop = input('Do you get any free drops? (y/n): ').lower().strip()
        if attendance_free_drop == 'yes' or attendance_free_drop == 'y':
            attendance_fd_amount = input('How many? ').strip()
            break
        elif attendance_free_drop == 'no' or attendance_free_drop == 'n':
            attendance_fd_amount = 'None'
            break
        else:
            print('\nERROR: Please enter yes or no.\n')

    class_time = {}
    while True:
        try:
            num_days = int(input('How many days do you have this class? (Enter \'0\' for ASYNC): '))
            break
        except ValueError:
            print('\nERROR: Please enter a number.\n')
    if num_days ==0:
        class_time['Online'] = ['Async']
    elif num_days>0:
        for days in range(0,num_days):
            day = input('Enter class week day: ').title().strip()
            time = input('Enter class week time: ').strip().upper()
            if day in class_time:
                class_time[day].append(time)
            else:
                class_time[day]=[time]

    print('\nNow adding grading scale...\n')
    print('- Enter section of grade or assignment name in this format: \'quizzes\' or \'final exam\'')
    print('- Enter weight in decimal format (.50,.15,etc): ')
    print('-------------------------------')
    total = 0
    assignments = {}
    while True:
        assignment_amount = input('\nHow many would you like to add?\n(Type \'skip\' to skip): ').strip().lower()

        if assignment_amount =='skip':
            break
        try:
            assignment_amount = int(assignment_amount)
        except ValueError:
            print('\nERROR. Please enter a number or skip.')
            continue
        if assignment_amount == 0:
            break
        for x in range(0,assignment_amount):
            assignment_name = input('\nEnter name: ').strip().title()
            while True:
                try:
                    weight = float(input('\nWeight for '+assignment_name+': '))
                    break
                except ValueError:
                    print('\nERROR. Please enter a the wait in decimal format (.50, .25, etc).')
            total += weight
            assignments[assignment_name] = weight
        if total > 1:
            print('\nThe total weight is not greater than or equal to 1.\nYour grades will not be calculated if the scale is incomplete.\nYou can add more sections later.\nWould you like to continue?')
            continuing = input('(y/n): ').lower().strip()
            if continuing == 'yes' or continuing == 'y':
                break
            elif continuing == 'no' or continuing == 'n':
                continue
            else:
                print('\nERROR: Please enter yes or no.\n')

    late_assignment = input('Enter the late assignment policy: ')

    location ={}
    building = input('\nEnter the building name or \'none\': ').title().strip()
    if building != 'None':
        room = input('\nEnter the room number of the class: ').strip().upper()
    else:
        room = 'NONE'

    location[building] = 'Room '+ room

    classes[class_name] = {
        'Contacts':{
            'Professor':professor_name,
            'Professor Email':prof_email,
            'T A': ta,
            'T A Email': ta_email,
        },
        'Policies': { #anotherkey of dicts
            'Attendance':attendance,
            'Free Drops For Attendance': attendance_fd_amount,
        },
        'Course Materials': materials,
        'Late Assignment Policy': late_assignment,
        'Assignments':assignments,
        'Class Time': class_time,
        'Class Location' : location
    }#brain is fried
    return classes

#save function for classes
def save_class(classes, filename):
    with open(filename, 'w') as f:
        json.dump(classes, f, indent=4)

#editing classes
def edit_class(classes,filename):
    while True:
        with open(filename, 'r') as f:
            classes = json.load(f)
        count = 1
        class_list = {}
        print('\n--------------\nEDITING\n--------------')
        for class_option in classes:
            print(count, '.', class_option)
            class_list[count] = class_option
            count += 1
        print('0 . BACK')

        try:
            choose = int(input('\nEnter number of class choice: '))
        except ValueError:
            print('\nPlease enter a number.')
            continue
        if choose ==0:
            break
        elif choose in class_list:
            class_name=class_list[choose]
            if class_name in classes:
                while True:
                    edit = input('\n--------------\nOPTIONS - Type \'exit\' at any time to go back.\n--------------\n1. Contacts\n2. Policies\n3. Grading Scale\n4. Class day or time\n5. Class Location\n\nWhat do you want to edit?').strip().lower()
                    if edit== 'exit':
                        return
                    if edit == '1': #contacts
                        contacts = classes[class_name]['Contacts']

                        while True:
                            print('\nCONTACTS\n------------')
                            for key,value in contacts.items():
                                print(key,': ',value)
                            choice_1 = input('Type what to edit: ').title().strip()
                            if choice_1 in contacts:
                                new_value = input('Enter the new info: ').title().strip()
                                contacts[choice_1] = new_value
                                save_class(classes, filename)
                            elif choice_1.lower()=='exit':
                                break
                            else:
                                print('\nERROR. Retype or exit.\n')
                    elif edit =='2': #policies
                        policies = classes[class_name]['Policies']
                        work_policy = classes[class_name]['Late Assignment Policy']
                        while True:
                            print('\nPOLICIES\n----------')
                            for key, value in policies.items():
                                print(key, ': ', value)
                            print('Late Assignment Policy: ', work_policy)

                            choice_2=input('\nType what to edit: ').title().strip()

                            if choice_2 in policies:
                                new_value = input('\nEnter the updated information: ').strip()
                                policies[choice_2] = new_value
                                save_class(classes, filename)

                            elif choice_2 =='Late Assignment Policy':
                                new_policy = input('\nEnter the updated information: ').strip()
                                classes[class_name]['Late Assignment Policy'] = new_policy
                                save_class(classes, filename)

                            elif choice_2.lower()=='exit':
                                break
                            else:
                                print('\nERROR. Retype or exit.\n')
                    elif edit == '3':#assignmnets
                        assignments = classes[class_name]['Assignments']
                        while True:
                            print('\nYour sections\n-----------------')
                            if len(assignments) == 0:
                                print('\nNo sections found.')
                                add_option = input('\nWould you like to add (y/n)? :')
                                if add_option =='n' or add_option =='no':
                                    break
                                elif add_option =='y' or add_option =='yes':
                                    while True:
                                        amount = input('\nHow many would you like to add (or exit)?: ').strip().lower()
                                        if amount == 'exit':
                                            break
                                        try:
                                            amount = int(amount)
                                        except ValueError:
                                            print('\nEnter a number amount or \'exit\' to go back.\n')
                                            continue
                                        for x in range(0, amount):
                                            assignment_name = input('Enter Section name: ').title().strip()
                                            while True:
                                                try:
                                                    weight = float(input('Enter the weight: '))
                                                    assignments[assignment_name] = weight
                                                    save_class(classes, filename)
                                                    break
                                                except ValueError:
                                                    print('\nERROR. Enter a weight in decimal format (.50, .25, etc).\n')
                                        break
                                else:
                                    print('ERROR. Enter yes, no, or exit.')
                            else:
                                for key, value in assignments.items():
                                    print(key, ': ', value)
                                assignment_menu = input('\n1. Edit name\n2. Edit weight\n3. Add Section\nYour choice: ').lower().strip()
                                if assignment_menu == '1': #edit name
                                    while True:
                                        change_name = input('\nEnter name to edit (or exit): ').title().strip()
                                        if change_name =='Exit':
                                            break
                                        if change_name in assignments:
                                            new_name = input('\nNew name: ').title().strip()
                                            assignments[new_name] = assignments.pop(change_name)
                                            save_class(classes, filename)
                                        else:
                                            print('\nERROR. Section not found. Please add by choosing \'3. Add section\' or retype.')
                                elif assignment_menu== '2': #edit weight
                                    while True:
                                        change_weight = input('Enter section name to edit (or exit): ').title().strip()
                                        if change_weight == 'Exit':
                                            break
                                        if change_weight in assignments:
                                            while True:
                                                try:
                                                    new_weight = float(input('Enter the new weight (ex: .25): '))
                                                    break
                                                except ValueError:
                                                    print('ERROR. Please enter a valid weight.')
                                            assignments[change_weight] = new_weight
                                            save_class(classes, filename)
                                            break
                                        else:
                                            print('\nERROR. Assignment not found. Please add in settings or retype.')
                                elif assignment_menu == '3':#add assignment
                                    while True:
                                        amount = input('\nHow many would you like to add (or exit)?: ').strip().lower()
                                        if amount == 'exit':
                                            break
                                        try:
                                            amount = int(amount)
                                        except ValueError:
                                            print('\nEnter a number amount or \'exit\' to go back.\n')
                                            continue

                                        for x in range(0, amount):
                                            assignment_name = input('Enter assignment name: ').title().strip()
                                            while True:
                                                try:
                                                    weight = float(input('Enter the weight (ex: .25): '))
                                                    assignments[assignment_name] = weight
                                                    save_class(classes, filename)
                                                    break
                                                except ValueError:
                                                    print('\nERROR. Please enter a valid weight.\n')
                                        break
                                elif assignment_menu == 'exit':
                                    break
                                else:
                                    print('\nERROR: Retype or exit.\n')
                    elif edit =='4':#add/edit class day/ time
                         class_time = classes[class_name]['Class Time']
                         while True:
                             print('\nClass Times\n-------------')
                             for key, value in class_time.items():
                                 print(key, ': ', value)
                             add_edit = input('\nPlease type \'add\', \'edit\', or \'exit\': ').strip().lower()
                             if add_edit == 'edit':
                                class_day= input('Enter the day to edit: ').title().strip()
                                if class_day in class_time:
                                    day_or_time = input('Edit the day or time?  ').strip().lower()
                                    if day_or_time == 'time':
                                        new_time = input('Enter new class time: ').strip().upper()
                                        class_time[class_day] = [new_time]
                                        save_class(classes, filename)
                                    elif day_or_time == 'day':
                                        new_day = input('Enter new class day: ').strip().title()
                                        class_time[new_day] = class_time.pop(class_day)
                                        save_class(classes, filename)
                                    elif day_or_time.lower() == 'exit':
                                        break
                                elif class_day == 'exit':
                                    break
                                else:
                                    print('ERROR: Retype or exit.')
                             elif add_edit == 'add':
                                new_day = input('Enter new class day: ').strip().title()
                                new_time = input('Enter new class time: ').strip().upper()
                                class_time[new_day] = [new_time]
                                save_class(classes, filename)
                             elif add_edit == 'exit':
                                 break
                             else:
                                print('ERROR: Retype or exit.')
                    elif edit =='5':#edit class location
                        location = classes[class_name]['Class Location']
                        while True:
                            print('\nLocations\n-------------')
                            for building,room in location.items():
                                print(class_name,'\n--------------\n',building, ': ', room)
                            add_edit = input('Add or edit a location (or exit)? Please type: ').strip().lower()
                            if add_edit == 'edit':
                                build_room = input('\nChange building or room: ').strip().lower()
                                if build_room =='building':
                                    old_building = input('\nEnter old building name: ').title().strip()
                                    if old_building in location:
                                        while True:
                                            new_build = input('\nEnter new building name: ').strip().title()
                                            location[new_build] = location.pop(old_building)
                                            save_class(classes, filename)
                                            print('\nLocation updated')
                                            break
                                    elif old_building=='Exit':
                                        break
                                    else:
                                        print('ERROR. Building not found. Retype or exit.')
                                        continue
                                elif build_room=='room':
                                    build = input('\nEnter building name: ').title().strip()
                                    if build in location:
                                        while True:
                                            room_num = input('\nEnter new room number: ').upper().strip()
                                            new_room = 'Room '+room_num
                                            location[build]=new_room
                                            save_class(classes, filename)
                                            print('Location updated')
                                            break
                                    elif build=='Exit':
                                        break
                                    else:
                                        print('ERROR. Building not found. Retype or exit.')
                                elif build_room=='exit':
                                    break
                                else:
                                    print('ERROR. Retype or exit.')
                            elif add_edit == 'add':
                                name= input('\nEnter the building name: ').title().strip()
                                room= input('\nEnter room number: ').upper().strip()
                                added_room = 'Room ' + room
                                location[name] = added_room
                                save_class(classes, filename)
                                print('Location added.')
                                break
                            elif add_edit == 'exit':
                                break
                            else:
                                print('ERROR. Retype or exit.')

                    else:
                        print('ERROR. Enter a valid choice or exit')
        else:
            print('\nERROR. Choose a valid class or \'0\'.')

#loading class
def load_classes(filename):
    try:
        with open(filename,'r') as f:
            classes = json.load(f)
            return classes
    except FileNotFoundError:
        return {}

