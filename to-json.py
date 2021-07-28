from data import goals, teachers
import json

with open("goals.json", 'w', encoding="utf-8") as f:
   json.dump(goals, f, ensure_ascii=False)

with open("teachers.json", 'w', encoding="utf-8") as f:
   json.dump(teachers, f, ensure_ascii=False)
