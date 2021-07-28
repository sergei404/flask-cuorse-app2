import json

def getGoals():
    goals = None
    with open("goals.json", "r", encoding='utf-8') as f:
        goals = json.load(f)
    return goals

def getTeachers():
    teachers = None
    with open("teachers.json", "r", encoding='utf-8') as f:
        teachers = json.load(f)
    return teachers

def getFilterTeachers(array, goal):
    new_array = []
    for i in array:
        if goal in i['goals']:
            new_array.append(i)
    return new_array

def getTeacher(array, id):
    for i in array:
        if i['id'] == id:
            return i

def getTeacherGoals(goals, teacher_goals):
    goals_str = ''
    for i in teacher_goals:
        goals_str += goals[i][0].split(' ')[1] + ' '

    return goals_str

weekdays = {
    'mon': ['Понедельник', 'monday'],
    'tue': ['Вторник', 'tuesday'],
    'wed': ['Среда', 'wednesday'],
    'thu': ['Четверг', 'thursday'],
    'fri': ['Пятница', 'friday'],
    'sat': ['Суббота', 'saturday'],
    'sun': ['Воскресенье', 'sunday'],
}

practice = {
    'l1': '1-2 часа в неделю',
    'l3': '3-5 часов в неделю',
    'l5': '5-7 часов в неделю',
    'l7': '7-10 часов в неделю'
}
