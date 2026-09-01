import json


def deleting(class_name):
    try:
        with open('classes.json') as f:
            classes = json.load(f)
    except Exception as e:
        print(e)
        classes={}

    if class_name in classes:
        confirm = input('Are you sure you want to delete', +class_name,+'? (y/n): ').lower().strip()
        if confirm == 'y' or confirm == 'yes':
            del classes[class_name]
            with open('classes.json', 'w') as f:
                json.dump(classes, f)
            print('\nClass deleted.')
            return
        elif confirm == 'n' or confirm == 'no':
            return
        else:
            print('ERROR. Please enter yes or no.')


