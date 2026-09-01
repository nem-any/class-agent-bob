from back_end import AI_QuickSearch_menu
from back_end import manual_menu
from back_end import settings
from back_end import deleting_class
from back_end import deleting_sem_sched
from calculators import calculate_menu

#Class Agent Bob Final Project

#There may be lots of bugs


print('\nWelcome to your Class Agent. What would you like to do?')


while True: #main menu
    print('\n-----------\nClass Agent Menu\n-----------')
    choice = input('1. Speak to Class Agent Bob (AI)\n2. Grades and GPA\n3. Settings\n0. EXIT\n\nEnter choice: ')
    if choice =='0': #exit
        print('\nThank you for using Class Agent.\nGoodbye!')
        break
    elif choice == '1': #bob
        AI_QuickSearch_menu()
        print('\n---Bob has left the chat---\n')
    elif choice =='2': #grades and gpa 
        calculate_menu() 
    elif choice =='3': #settings
        while True:
            print('\n--------------\nSETTINGS\n--------------')
            print('1. View current information.')
            print('2. Add or Edit information.')
            print('3. Delete')
            print('0. Back')
            enter = input('\nEnter choice: ')
            if enter =='0':
                break
            if enter =='1':
                manual_menu()
                break
            elif enter =='2':
                settings()
                break
            elif enter =='3':
                while True:
                    choose = input('\n1. Delete class\n2. Delete schedule\n0. Back')
                    if choose == '1':
                        deleting_class()
                        break
                    elif choose == '2':
                        deleting_sem_sched()
                        break
                    elif choose == '0':
                        break
                    else:
                        print('Please enter a valid choice.')
                        continue
                    break
            else:
                print('Please enter a valid choice.')
    else:
        print('Please enter a valid choice.')

'''
saving this for later
"2027": {
        "Spring": {
            "schedule of classes available": "OCT 12",
            "registration period": "OCT 26 - JAN 10",
            "classes begin": "JAN 11",
            "late registration period": "JAN 11 - JAN 15",
            "midpoint": "MAR 02",
            "end of classes": "APR 26",
            "exam period": "APR 27 - MAY 4",
            "final grades available": "MAY 6"
'''