from google import genai
import json

client = genai.Client(api_key="api key")

model = 'gemini-3.6-flash' #may need to update model if out of date

#pip install google-genai
#client.models.generate_content( model = 'model name',contents = '''enter ai prompt''')

def loading_file(filename,obj): #loading info from the JSON files function
    try:
        with open(filename) as f:
            obj = json.load(f)
            return obj
    except FileNotFoundError:
        return {}

def gem_greeting(): #bob greet
    greeting = client.models.generate_content(
        model=model,
        contents='''
        introduce yourself as class agent named \'Bob\'.
        ask student how you can help them today.
        use a cowboy accent.
        make it short and direct.
        '''
    )
    return greeting.text

def Bob(student_q): #bob DB
    yearly_schedule = loading_file(filename='2026.json',obj='year_schedule')
    breaks_and_holidays = loading_file(filename='breaks_holidays.json',obj='no_school_days')
    all_classes = loading_file(filename='classes.json',obj='classes')
    class_grades = loading_file(filename='class_grades.json', obj='class_grades')
    gradebook_data = loading_file(filename='gradebook.json', obj='gradebook')

    gpa_data = loading_file(filename='gpa.json', obj='gpa')

    q = student_q.lower()
    if any(word in q for word in ['gpa','GPA']):
        student_data = {
            'gpa': gpa_data, #doing this so bob doesn't overload
        }

    else:
        student_data = {
            'school_schedule': yearly_schedule,
            'classes': all_classes,
            'holidays/breaks (no class days)': breaks_and_holidays,
            'grade book for classes': gradebook_data,
            'class grades': class_grades,
        } 

    context = json.dumps(student_data, indent=2) #string dump

    answer = client.models.generate_content(
        model=model,
        contents=('''
    
        you are a helpful student assistant and basically a speedy syllabus. 
        answer shortly, directly, in one sentence, always with a cowboy accent.
        
        use ONLY this data:'''+context+'''

        if the answer is not in the data provided, say you cannot find it. Recommend they add the data in settings.
        
        student question:'''+student_q+'''
        
        if the user types \'quit\', tell them bye.'
        
        '''
                )
    )
    return answer.text

def gem_adios(student_q): #bye bob
    farewell = client.models.generate_content(
        model=model,
        contents='''
        If the user types \'quit\' in:
        ''' +student_q+'''
        
        tell them bye in a cowboy accent. 
        Make it short, direct, in one sentence.
        '''
    )
    return farewell.text